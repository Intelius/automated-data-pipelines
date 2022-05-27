import sys
sys.path.append("./dags/")

from src.setupconfig import Configservice 
from src.dataservice import Dataservice
import pandas as pd
from pytz import timezone
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import time
import yaml

##----------------------- 1. Intialization block-----------------------##   
try:
    ## Initialization 
    confg = Configservice()
    dsvc = Dataservice()
    tickers = ','.join(confg.getTickerList())
    tz = timezone('US/Eastern')
    utc = timezone('UTC')
except Exception as e:
    logging.error('error in initialization')
    logging.error(e)    


def extract_news_df():
    try:
        df = pd.DataFrame()
        dataconfigyml = open("dags/src/dataconfig.yml")
        dataconfig = yaml.load(dataconfigyml, Loader=yaml.FullLoader)
        engine_news = create_engine(dataconfig['mysqlsettings']['dairdb'])
        db_name = 'news_description'
        t1 = datetime.now(tz)-timedelta(minutes=5)
        t1_str = t1.strftime('%Y-%m-%d %H:%M:%S')
        sql = f"SELECT * FROM  {db_name} where posttime >= '{t1_str}'"
        df = pd.read_sql(sql, con=engine_news)
        print('data read complete')
        print(df)
        engine_news.dispose()
    except Exception as e:
        logging.error('error in calling polygon io API')
        logging.error(e)
    return df


##----------------------- Start of - 2. News Ingestion Function  -----------------------##

def DailyNewsPolygonMain(**kwargs):
    source ='Polygon IO'
    try:  
        time.sleep(60)
        print("Read news from db, starts:".format(source)) 
        tickers_list = tickers.split(",") 
        news_df = extract_news_df()
        if not news_df.empty:
            for i in range(len(news_df)):
                df = news_df.iloc[[i]]
                # Add sentiments (calling prediction news sentiment)
                if not df.empty : 
                    for ticker in tickers_list:
                        ticker_str = '\'' + ticker + '\''
                        if ticker_str in df.loc[df.index[0],'tickers']:
                            print(ticker_str)
                            try:                       
                                post_pl ={
                                    "ticker": ticker,
                                    "title": df.loc[df.index[0],'title'],
                                    "news_url" : df.loc[df.index[0],'article_url'],
                                    "news_content": df.loc[df.index[0],'description'],
                                    "summary": " ",
                                    "id": df.loc[df.index[0],'id'],
                                    "datetime": str(df.loc[df.index[0],'datetime'])
                                }      
                                print("***********Calling Sentiment Prediction API for ticker: {}, date: {}".format(ticker, datetime.now(utc)))
                                returnmsg = dsvc.callgraviteeapi("predict_news_sentiment", post_pl)                        
                                print("Sentiment Prediction API response: " + returnmsg)                 
                            except Exception as e:  
                                logging.error("Error in calling sentiment prediction description: " + str(e))   
                else:
                    logging.info('No New News from Polygon IO in the past 5 minutes') 
    except Exception as e:  
        logging.error("Error description in processing: " + str(e))    
  


##----------------------- End of - 2. News Ingestion Function  -----------------------##
if __name__ == "__main__":
    DailyNewsPolygonMain()
