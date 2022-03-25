import os
import csv

from click import prompt
import openai

listemotion = []

# with open('EmotionsList.csv') as csvfile:
#    reader = csv.reader(csvfile, delimiter=',')
#    for word in reader:
#        listemotion.append(word)
PROMPTS = """How is A feeling in the following conversation ?
A: Hey ! How are you ? Would you be free to talk ?
B: Hey, unfortunately I can't today :( maybe tomorrow ? 
A: no no it's alright I don't want to bother you

A's is feeling shy
--
How is A feeling in the following conversation ?
A: Hey mate, I didn't like how you acted before it was very selfish
B: What the fuck are you talking about, I didn't do anything

A's feeling injustice
--
How is B feeling in the following conversation ?
A: fuck you !

B's feeling aggressed
--
How is B feeling in the following conversation ?
B: Man, I've been waiting for 30 minutes now..
A: Sorry, my bus was late
B: Come on, what a lame excuse

B's feeling annoyed
--
How is B feeling in the following conversation ?
A: I am so happy for the good news you told me !
B: Thank man, I really worked hard for it :) 
A: You deserve it

B's feeling proud
--
"""
A_FEEL_B = "How is A feeling in the following conversation ?"
B_FEEL_B = "How is B feeling in the following conversation ?"


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

        prompts.append(PROMPTS + A_FEEL_B + "\n" + conv)
        prompts.append(PROMPTS + B_FEEL_B + "\n" + conv)

        return prompts

    def get_emotions_completion(self):
        prompts = self.to_prompts()
        resp = []

        for pr in prompts:
            print(pr)
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

    def get_emotions_classification(self, preprocess_message):
        swag = openai.Classification.create(
            search_model="ada",
            model="curie",
            query=preprocess_message,
            examples=[
                ["I am sad", "sad"],
                ["I feel awesome", "happy"],
                ["I did not expect that", "suprise"],
                ["It is boring", "bored"],
                ["It really scares me", "fear"],
                ["I want to punch someone", "angry"],
                ["I do not understand", "confused"],
                ["I do not want to speak about it", "irritated"],
                ["You really disappointed me", "disappointed"],
                ["I am exhausted", "tired"],
                ["I am feeling frustrated", "frustration"]
            ],
        )

        return swag

    def fromMessageToSingleWord(self, message):
        self.add_message(message)
        answers_tmp = self.get_emotions_completion()
        # print(answers_tmp)
        # answers = []
        # for answer in answers_tmp:
        #     answer = answer.replace('\n', "")
        #     answers.append(self.get_emotions_classification(answer))

        # yoloDict = {
        #     "A": answers[0]['label'],
        #     "B": answers[1]['label'],
        # }
        return answers_tmp


def get_emotions(conversation: str):

    #"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"
    #openai.api_key = "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
    openai.api_key = "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"

    c = Conversation()

    final = c.fromMessageToSingleWord(conversation)
    print(final)
    return final


# get_emotions("")
    #OLD ONE "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
