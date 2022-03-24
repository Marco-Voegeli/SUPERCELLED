import os
import csv

from click import prompt
import openai

listemotion = []

with open('EmotionsList.csv') as csvfile: 
    reader = csv.reader(csvfile, delimiter=',')
    for word in reader:
        listemotion.append(word)
        

print(listemotion)
#GEN_FEEL_B = "What are the feelings in the following conversation between A and B ?"
#GEN_FEEL_E = "Conversation's emotions:"
# A_FEEL_B = "How is A feeling in the following conversation:"
#A_FEEL_B = "What are the feelings of A in the following conversation ?"
#A_FEEL_E = "A's two most prominent emotions:"

#A_FEEL_EMOJI = "What would be the best emoji to describe A's most proeminent emotion?"

#B_FEEL_B = "What are the feelings of B in the following conversation ?"
# B_FEEL_B = "How is B feeling in the following conversation:"
#B_FEEL_E = "B's two most prominent emotions:"
#B_FEEL_EMOJI = "What would be the best emoji to describe B's most proeminent emotion?"

A_FEEL_ONE = "Using only one single word, express A's emotion: "
B_FEEL_ONE = "Using only one single word, express B's emotion: "


class Conversation:
    def __init__(self) -> None:
        self.messages = []

    def add_message(self, msg: str):
        self.messages.append(msg + "\n")
        
    def clear(self):
        self.messages = []
        

    def get_emotions_oneWord(self):
        messages = self.messages
        resp = []

        for message in messages:
            # print(pr)
            # print("-"*10)
            resp.append(openai.Classification.create(
                search_model="ada",
                model="curie",
                query="I am tired",
                labels=[["I am sad","sad",]
    ["I feel awesome","happy",]
    ["I did not expect that","suprise",]
    ["It is boring","bored"]
    ["It really scares me","fear",]
    ["I want to punch someone","angry"]
    ["I do not understand","confused"]
    ["I do not want to speak about it","irritated"]
    ["You really disappointed me","disappointed"]
    ["I am exhausted","tired",]],
            ))
        
        return resp    


openai.api_key = "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"

c = Conversation()

c.add_message("A: I am tired today, would you like to talk ?")

##c.get_emotions()
answers = c.get_emotions_oneWord()

print(answers)
    
