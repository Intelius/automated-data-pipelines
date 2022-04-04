
import sys
sys.path.append("./src/newssentiment-service")
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
import pandas as pd
from src.news_main import  prediction_service
import time
from datetime import  datetime
import pytz
from sqlalchemy import create_engine
from tensorflow import keras
import logging

app = FastAPI( title="News Sentiment Prediction Service APIs ",
        description="APIs for processing News by Ticker.",
        version="1.0.0")

# define the path to the model inside the repo
path = 'model_news/news/news_sentiment_artifacts/artifacts/sentiment-prediction/data_news/model'
model = keras.models.load_model(path)

###################################################################
## Sentiment Prediction Iput Class###
###################################################################
class News_Details(BaseModel):
    ticker: str
    title: str
    news_url: str
    news_content: str
    summary: str
    id: str
    datetime: str

# This function is used to convert the news object to a dictionary compatible with the keys used in the other functions
def get_News_dict(news):
    news_dict =   dict([
                    ("ticker", news.ticker),
                    ('title', news.title),
                    ("news_url",news.news_url),
                    ("content",news.news_content), 
                    ("text",news.summary),
                    ("id", news.id),
                    ("datetime", news.datetime)]) 
    return news_dict

###################################################################
# Define the FAST API function
###################################################################

@app.post('/predict_news_sentiment')

def predict_main(news: News_Details):

    try:
        # Prepare data recived from API call for the sentiment prediction function
        start_time = time.time()
        news_df = pd.DataFrame.from_dict(get_News_dict(news), orient='index').T
        
        published_time = pd.to_datetime(news_df.loc[news_df.index[-1],'datetime'])
        news_df['time']= datetime.strftime(published_time, "%H:%M:%S")
        news_df['date'] = datetime.strftime(published_time, "%Y-%m-%d")
        
        # Calling the sentiment prediction function
        ps = prediction_service(news_df)
        result = ps.prediction_service_sentiment(model= model)

        # Prepare the predicted result for saving them in db
        db_result = result[['ticker',  'id', 'datetime' , 'final_score', 'predicted_label']].copy()

        db_result['sector'] = ""
        db_result.rename(columns={'predicted_label':'sentiment_score', 'final_score':'compound_influence_score'}, inplace=True)
        db_result['posttime'] = datetime.now(pytz.timezone('US/Eastern'))
        try:
            db_result.drop(['date','time'], axis=1, inplace= True)  # remove redundant columns
        except:
            pass
        # Save results in DB
        try:
            path = 'mysql+pymysql://root:BoosterPack202!@my-release-mysql.data.svc.cluster.local:3306/dair_boosterpack'
            prediction_mysql_engine = create_engine(path)
            db_result.to_sql(con=prediction_mysql_engine, name="news_sentiment_prediction", if_exists='append', index=False)
            prediction_mysql_engine.dispose()
        except Exception as e:
            print(e)
            print(db_result)
        response = result.to_json()

    except Exception as e:
        response = str(e)
        logging.info('error {}'.format(str(e)))
        logging.info("Processed Time: --- %s seconds --- " % (time.time() - start_time))
        return response


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=6022)   


