import sys
sys.path.append("./dags/")

import time
from datetime import datetime, timedelta
from pytz import timezone
import logging
import yaml
import pandas as pd
from src.setupconfig import Configservice 
from src.kafkaservices import sendmessagetokaf

try:
    tz = timezone('US/Eastern')
    utc = timezone('UTC')
    confg = Configservice()
    dataconfigyml = open("dags/src/dataconfig.yml")
    dataconfig = yaml.load(dataconfigyml, Loader=yaml.FullLoader)
    tickers = ','.join(confg.getTickerList())
except:
    print('Error initializing the pipeline!')

def sendmindatatokafka(aggrlvl, savedStatus, msgstarttime, itopic, imsg):
    #Kafka msg 
    try:
        topic = ""
        if itopic == "ingestion1min":
            topic = 'dair-dataingestion-1min-topic' 
        print("message sent to Kafka: {}".format(str(imsg)) )    

        sendmessagetokaf(
            aggrlvl,\
            savedStatus,\
            msgstarttime,\
            str(datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')),\
            topic,
            0,\
            tz,\
            imsg)    
                           
    except Exception as e:              
        print("Error sending message to kafka... errorcode={}".format(str(e))) 
        pass

def unix_to_time(time):
    return datetime.fromtimestamp(time, tz=tz)

def convert_unix_in_df(df,input_column,output_column):
    df[output_column] = df[input_column].apply(lambda x : unix_to_time(x))
    return df

def datetime_to_unix():
    d = datetime.now().replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    d2 = datetime.now() - timedelta(minutes=1)
    d2= d2.replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    d = datetime.strptime(d,'%Y-%m-%d %H:%M:%S')
    d2 = datetime.strptime(d2,'%Y-%m-%d %H:%M:%S')
    unixtime_start = time.mktime(d2.timetuple())
    unixtime_end = time.mktime(d.timetuple())
    return str(int(unixtime_start)), str(int(unixtime_end))

def finn_hub_api_call(ticker):
    import requests
    timestamp_start, timestamp_end = datetime_to_unix()
    finnhub_token = confg.getFinnhubToken()
    if finnhub_token=="":
        print('Finnhub.io token has not been stored yet as an Airflow variable! Please refer to the documentation.')
        return None
    
    url = dataconfig['finnhub']['apiurl'] + ticker + '&resolution=1&from=' + timestamp_start + '&to=' + timestamp_end + '&token=' + finnhub_token
    
    try:
        r = requests.get(url)
        data = r.json()
        return  pd.DataFrame.from_dict(data)
    except:
        print('Error calling Finnhub API!')


def marketdataingestion():
    tickers_list = tickers.split(",") 
    i=1
    for ticker in tickers_list:
        try:
            df = finn_hub_api_call(ticker= ticker) 
            if df is not None:
                df['ticker'] = ticker
                df=df.rename(columns={'c':'close', 'l':'low', 'h':'high', 'o': 'open', 't':'timestamp', 'v':'volume'})
                df.loc[df.index[0],'timestamp']= unix_to_time (df.loc[df.index[0],'timestamp'])
                # send the kafka massage to the topic
                
                if not df.empty:
                    try:
                        sendmindatatokafka(aggrlvl='1min', savedStatus=1, \
                            msgstarttime= datetime.now(tz), itopic='ingestion1min', imsg=df)
                    except Exception as e:
                        logging.error(e)
        except:
            print("Error ingesting data for ticker: "+ticker)
            pass