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

listemotion = []

#with open('EmotionsList.csv') as csvfile: 
#    reader = csv.reader(csvfile, delimiter=',')
#    for word in reader:
#        listemotion.append(word)
        

A_FEEL_B = "How is A feeling in the following conversation:"
B_FEEL_B = "How is B feeling in the following conversation:"


#A_FEEL_EMOJI = "What would be the best emoji to describe A's most proeminent emotion?"



class Conversation:
    def __init__(self) -> None:
        self.messages = []
        self.yolo=openai.File.create(file=open("exampleEmotion.jsonl"), purpose="classifications") 
        
               
    def add_message(self, msg: str):
        self.messages.append(msg + "\n")
        
    def clear(self):
        self.messages = []
        
    def to_prompts(self):
        prompts = []
        conv = ""
        for msg in self.messages:
            conv += msg
            
        prompts.append(A_FEEL_B + "\n" + conv)
        prompts.append(B_FEEL_B + "\n" + conv)
        
        return prompts
        
    def get_emotions_completion(self):
        prompts = self.to_prompts()
        resp = []

        for pr in prompts:
            # print(pr)
            # print("-"*10)
            resp.append(openai.Completion.create(
                engine="text-davinci-002",
                prompt=pr,
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0)["choices"][0]["text"]
            )

        return resp 

    def get_emotions_classification(self,preprocess_message):            
        swag = openai.Classification.create(
                file=self.yolo,
                search_model="ada",
                model="curie",
                query=preprocess_message,
                max_examples=3,      
        )  
        return swag
    
    def fromMessageToSingleWord(self,message):
        self.add_message(message)
        answers_tmp = self.get_emotions_completion()
        answers = []
        for answer in answers_tmp:
            answer = answer.replace('\n',"")
            answers.append(self.get_emotions_classification(answer))
        
        yoloDict = {
            "A": answers[0]['label'],
            "B": answers[1]['label'],
        }  
        return yoloDict
        
 
def get_emotions(conversation : str):

    openai.api_key = "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"
    c = Conversation()

    final = c.fromMessageToSingleWord(conversation)
    print(final)   
    return final 

#tibo = get_emotions("I don't know why, but this man told me that he wanted to eat some fries, but I am not really interested in doing that")
#print(tibo)


