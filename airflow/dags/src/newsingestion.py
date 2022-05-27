import sys
from xxlimited import new
sys.path.append("./dags")
import json
from src.setupconfig import Configservice 
import pandas as pd
from pytz import timezone
from urllib.request import urlopen
import logging
from datetime import datetime, timedelta
import yaml
from sqlalchemy import create_engine

##----------------------- 1. Intialization block-----------------------##   
tickers = []
try:
    ## Initial config
    confg = Configservice()
    print(confg)
    tickers = ','.join(confg.getTickerList())
    tz = timezone('US/Eastern')
    utc = timezone('UTC')
    print(utc)
except Exception as e:
    print(e) 

def extract_news_df_polygonio(api_key):
    try:
        dataconfigyml = open("dags/src/dataconfig.yml")
        dataconfig = yaml.load(dataconfigyml, Loader=yaml.FullLoader)
        df = pd.DataFrame()
        print(datetime.now(utc))
        # define a start time to fetch all the news for any ticker
        start_time=datetime.now(utc)-timedelta(minutes=15,seconds=5)
        start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S') 
        print(start_time_str)
        link1 = dataconfig['polygon']['apiurl']  + str(start_time_str) + '&apiKey=' + api_key 
        response = urlopen(link1)
        elevations = response.read()
        data = json.loads(elevations)
        df = pd.DataFrame.from_dict(data['results'])
    except Exception as e:
        print('error in calling polygon io API')
        print(e)
    return df

def db_preparation(df):
    try:
        for index, row in df.iterrows():                       
            new_df= pd.DataFrame( [[row['id'],row['title'], row['author'], row['article_url'], \
                row['description'], row['publisher']['name'], str(row['tickers']), str(row['keywords']),\
                     datetime.strptime(row['published_utc'], "%Y-%m-%dT%H:%M:%SZ"), datetime.now(tz=utc).strftime('%Y-%m-%d %H:%M:%S'), str(row['image_url'])]], columns=[ 'id',
                        "title",  "author",  "article_url", \
                        "description", "publisher",  "tickers",  "keywords", "published_utc", 'posttime', 'image_url'])
    except Exception as e:
        print('error in preparation data:' + str(e))
        return pd.DataFrame()
    return new_df

def  DailyNewsPolygonMain(**kwargs):
    try:  
        confg = Configservice()
        tickers = ','.join(confg.getTickerList())
        print("Read ticker news live data from API every 5 mins from Polygon, starts:") 
        tickers_list = tickers.split(",") 
        
        polygonToken = confg.getPolygonToken()
        if polygonToken=="":
            print('Polygon.io token has not been stored yet as an Airflow variable! Please refer to the documentation.')
            return
        
        # read the news from Polygon IO (calling API)
        news_df = extract_news_df_polygonio(api_key = polygonToken)
        
        if not news_df.empty :            
            for i in range(len(news_df)):
                # add the news if it is the ticker we want
                tickers_1=news_df.loc[news_df.index[i],'tickers']
                for ticker in tickers_1:
                    if ticker in tickers_list:
                        print("Saving news for ticker:"+ticker)
                        df = news_df.iloc[[i]]
                        print(df.columns)
                        df = db_preparation(df = df)
                        print(df.columns)
                        df['datetime'] = pd.to_datetime(df.published_utc)
                        df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern').dt.tz_localize(None)
                        df = df.drop(labels='published_utc', axis= 1)
                        # save in db
                        dataconfigyml = open("dags/src/dataconfig.yml")
                        dataconfig = yaml.load(dataconfigyml, Loader=yaml.FullLoader)
                        prediction_mysql_engine = create_engine(dataconfig['mysqlsettings']['dairdb'])
                        if not df.empty:
                            try:
                                df.to_sql(con=prediction_mysql_engine, name="news_description", if_exists='append', index=False)
                            except Exception as e:
                                logging.error(e)
                        prediction_mysql_engine.dispose()
        else:
            logging.info('No new news from polygon')
    except Exception as e:
        print('error in main:')
        print(e)

if __name__ == "__main__":
    DailyNewsPolygonMain()


