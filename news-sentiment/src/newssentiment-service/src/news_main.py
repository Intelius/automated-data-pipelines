import sys
sys.path.append("./src/newssentiment-service")
from src.news_utils import text_to_word_sequences_wrapper
from tensorflow.keras.preprocessing.sequence import pad_sequences
from news_preprocess import news_sentiment_preprocessing as nsp
from keras_preprocessing.sequence import pad_sequences
from pytz import timezone

jtz=timezone('US/Eastern')

###################################################################
# Define prediction class
###################################################################
class prediction_service:

    def __init__(self, input_data):
        self.input_df = input_data

    def prediction_service_sentiment(self, model):
        from datetime import datetime
        print('initialize sentiment prediction at '  +  datetime.now(jtz).strftime("%H:%M:%S"))
        df = nsp().main_preprocess(self.input_df) # TODO: use the same preprocessing as the one for training data
        df.processed_text.fillna(" ", inplace=True)
        sequences = df.processed_text.apply(text_to_word_sequences_wrapper)
        padded_data = pad_sequences(sequences, maxlen=100)
        print("test data loaded."  +  datetime.now(jtz).strftime("%H:%M:%S"))
        predictions = model.predict(padded_data)
        df['final_score'] = predictions[:, [2]] - predictions[:, [0]]
        class_names = ['Negative', 'Neutral', 'Positive']
        df['predicted_label'] = [class_names[i] for i in list(predictions.argmax(axis=-1))]
        print('sentiment prediction finished'  +  datetime.now(jtz).strftime("%H:%M:%S"))
        return df

