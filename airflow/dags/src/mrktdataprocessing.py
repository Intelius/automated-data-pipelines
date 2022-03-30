import sys
sys.path.append("./dags/")
from src.setupconfig import Configservice 
from dagutils import checkmarkethrs
from src.kafkaservices import initializakafkaconsumer
from datetime import datetime
from pytz import timezone
from sqlalchemy import create_engine
import yaml
import json
import pandas as pd
from finta import TA

##----------------------- Intialization block-----------------------##   

try:
    tz = timezone('US/Eastern')
    table_name = 'marketdata_1minute'
    confg = Configservice()
    dataconfigyml = open("dags/src/dataconfig.yml")
    dataconfig = yaml.load(dataconfigyml, Loader=yaml.FullLoader)
    tickers = ','.join(confg.getTickerList())
    consumer = initializakafkaconsumer('dair-dataingestion-1min-topic', 'processing_1min')
    print('Initialization Complete!')
except Exception as e:
    print('Error in initialization block! Description:'+str(e))
    

def read_data(tbl_name, ticker, msg_datetime):
    try:
        dairdb_mysql_engine = create_engine(dataconfig['mysqlsettings']['dairdb'])
        t1 = datetime.now(tz).replace(hour=4,minute=0,second=0).strftime('%Y-%m-%d %H:%M:%S')
        sql = f"SELECT * FROM  {tbl_name} where datetime >= '{t1}' and datetime < '{msg_datetime}' and ticker='{ticker}'"
        print("SQL commmad for reading data: " + sql)
        df = pd.read_sql(sql, con=dairdb_mysql_engine)
        return df
    except Exception as e:
        print('Error reading previous data! Description: '+str(e))
        return pd.DataFrame()

 
def marketdataprocessing():
    try:
        for message in consumer:
            if (not checkmarkethrs()):
                break
            
            try:    
                # Prepare the received data        
                a = message.value
                print("Consumed massage: "+ a)
                payload = json.loads(a)
                df = pd.DataFrame([[payload['ticker'], float(payload['high']),\
                        float(payload['low']), float(payload['open']),\
                        float(payload['close']), int(payload['volume']), \
                        payload['timestamp'], 0]],\
                    columns=['ticker', 'high', 'low', 'open', 'close', 'volume', 'datetime','EMA9'])
            
                df_prev = read_data(table_name, payload['ticker'], payload['timestamp'])
               
                if len(df_prev)>=9:
                    
                    temp_df = pd.concat([df_prev, df], ignore_index=True, sort=False)
                    temp_df.datetime = pd.to_datetime(temp_df.datetime)
                    temp_df.set_index('datetime', inplace=True)
                    df['EMA9'] = TA.EMA(temp_df, 9).iloc[-1]
                    print('Calculated EMA based on previous candlesticks!')
                else:
                    print('Used close price as EMA9!')
                    df['EMA9'] = float(payload['close'])
            except Exception as e:
                print('Error processing data! Description: '+str(e))
                
            # save data in DB
            try:
                dairdb_mysql_engine = create_engine(dataconfig['mysqlsettings']['dairdb'])
                df.to_sql(con=dairdb_mysql_engine, name=table_name, if_exists='append', index=False)
                print('Successfully saved data in  DB. Ticker: {}'.format(payload['ticker']))
            except Exception as e:
                print('Error saving data in DB! Description:'+str(e))
                
    except Exception as e:
        print('Error consuming kafka messages! Exiting the dag run. Description:'+str(e))
        