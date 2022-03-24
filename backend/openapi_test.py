import os
import csv

from click import prompt
import openai

listemotion = ""

with open('EmotionsList.csv') as csvfile: 
    reader = csv.reader(csvfile, delimiter=',')
    for word in reader:
        listemotion += (word[0]) + ", "
        


GEN_FEEL_B = "What are the feelings in the following conversation between A and B ?"
GEN_FEEL_E = "Conversation's emotions:"
# A_FEEL_B = "How is A feeling in the following conversation:"
A_FEEL_B = "What are the feelings of A in the following conversation ?"
A_FEEL_E = "A's two most prominent emotions:"

A_FEEL_EMOJI = "What would be the best emoji to describe A's most proeminent emotion?"

B_FEEL_B = "What are the feelings of B in the following conversation ?"
# B_FEEL_B = "How is B feeling in the following conversation:"
B_FEEL_E = "B's two most prominent emotions:"
B_FEEL_EMOJI = "What would be the best emoji to describe B's most proeminent emotion?"

A_FEEL_ONE = "Using only one single word, express A's emotion: "
B_FEEL_ONE = "Using only one single word, express B's emotion: "
C_FEEL_ONE = "Using only one single word, express C's emotion: "


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
        prompts.append(GEN_FEEL_B + "\n" + conv + "\n" + GEN_FEEL_E)
        prompts.append(A_FEEL_B + "\n" + conv + "\n" + A_FEEL_E)
        prompts.append(B_FEEL_B + "\n" + conv + "\n" + B_FEEL_E)
        
        return prompts
        
    def to_prompts_one(self):
        prompts = []
        conv = ""
        for msg in self.messages:
            conv += msg
        prompts.append(A_FEEL_ONE + "\n" + conv)
        prompts.append(B_FEEL_ONE + "\n" + conv)
        prompts.append(C_FEEL_ONE + "\n" + conv)

        for prompt in prompts:
            print(prompt)
        return prompts

    def get_emotions(self):
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

        for res in resp:
            print("*" * 10)
            print(res)
            print("-" * 10)
        return res

    def get_emotions_oneWord(self):
        prompts = self.to_prompts_one()
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


openai.api_key = "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"

c = Conversation()

c.add_message("A: I am tired today, would you like to talk ?")
##c.get_emotions()
answers = c.get_emotions_oneWord()

toSend = []
for answer in answers:
    tmp = answer.replace('\n',"")
    tmp = tmp.replace(' ', "")
    tmp = tmp.replace('', "")

    toSend.append(tmp[2:])
    
print(toSend)
