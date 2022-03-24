import os
import csv

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
                search_model="ada",
                model="curie",
                query=preprocess_message,
                examples=[
                        ["I am sad","sad"],
                        ["I feel awesome","happy"],
                        ["I did not expect that","suprise"],
                        ["It is boring","bored"],
                        ["It really scares me","fear"],
                        ["I want to punch someone","angry"],
                        ["I do not understand","confused"],
                        ["I do not want to speak about it","irritated"],
                        ["You really disappointed me","disappointed"],
                        ["I am exhausted","tired"],
                        ["I am feeling frustrated","frustration"]
                        ],
            )
        
        return swag
    
    def fromMessageToSingleWord(self,message):
        self.add_message(message)
        answers_tmp = self.get_emotions_completion()
        print(answers_tmp)
        answers = []
        for answer in answers_tmp:
            answer = answer.replace('\n',"")
            answers.append(self.get_emotions_classification(answer))
        
        yoloDict = {
            "A": answers[0]['label'],
            "B": answers[1]['label'],
        }  
        return yoloDict
        
 


openai.api_key = "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"

c = Conversation()

final = c.fromMessageToSingleWord("A: Would you kindly fuck off mate?")
print(final)   
