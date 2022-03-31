from nltk import TreebankWordTokenizer

# preprocessing the input text
class news_sentiment_preprocessing:
    def __init__(self):
        pass
    
    def main_preprocess(self,input_df):
        tokenizer = TreebankWordTokenizer()
        input_df['processed_text'] = input_df['title'].apply(tokenizer.tokenize).apply(lambda tokens: ' '.join(tokens))
        return input_df


