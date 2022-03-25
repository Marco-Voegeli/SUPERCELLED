import os
import csv
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam


from sklearn.preprocessing import LabelEncoder

import re 
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences

nltk.download('stopwords')
stopwords = set(nltk.corpus.stopwords.words('english'))




from click import prompt
import openai

class TestKeras:
    def __init__(self) -> None:
        self.model = Sequential()
        self.model.add(Embedding(input_dim=10000, output_dim=150, input_length=150))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(128))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(64, activation="sigmoid"))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(6, activation="softmax"))
        self.model.load_weights('model.h5')
        
    def text_prepare(self,text):
        stemmer = PorterStemmer()
        corpus = []
    
        text = re.sub("[^a-zA-Z]", " ", text[0])
            
        text = text.lower()
        text = text.split()
            
        text = [stemmer.stem(word) for word in text if word not in stopwords]
        text = " ".join(text)
            
        corpus.append(text)
        one_hot_word = [one_hot(text, n=10000)]
        embeddec_doc = pad_sequences(sequences=one_hot_word,
                                maxlen=150,
                                padding="pre")
        
        return embeddec_doc

    def predict(self,text):
        lb = LabelEncoder()
        #text = lb.fit_transform(text)

        text = self.text_prepare(text)
        
        output = self.model.predict(text)
        
        
        return output

test = TestKeras()
result = test.predict(["I want to eat some fries because I hate you and your whole family"])
print(result) #sad, anger, love, surprise,fear,joy

