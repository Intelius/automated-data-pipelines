import os
fileDir = os.path.dirname(os.path.realpath('__file__'))

WORD_EMBEDDING_ADDRESS_1 =os.path.join(fileDir,\
    'src/input/glove.6B.100d.txt')

import numpy as np
from tensorflow.keras.preprocessing.text import text_to_word_sequence

word_index = None
embedding_indexer = None

def get_embedding_indexer():
    global embedding_indexer
    if embedding_indexer is None:
        embedding_indexer = {}
        f = open(WORD_EMBEDDING_ADDRESS_1, encoding='UTF-8')
        for line in f:
            values = line.split()
            word = values[0]
            value = np.asarray(values[1:], dtype='float32')
            embedding_indexer[word] = value
        f.close()
    return embedding_indexer

def get_word_index():
    global word_index
    if not word_index:
        embedding_indexer = get_embedding_indexer()      
        word_index = {w: i for i, w in enumerate(embedding_indexer.keys(), 1)}
    return word_index

def text_to_word_sequences_wrapper(texts):
    word_index = get_word_index()
    tokens = text_to_word_sequence(texts)
    return [word_index.get(w) for w in tokens.copy() if w in word_index.copy()]

