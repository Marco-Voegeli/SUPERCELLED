# CHATMO - STARTHACK 2022

### Introduction
This project was developped during [StartHack](https://www.starthack.eu/program). 

## SUPERCELL CASE

Bringing non verbal communication to the virtual world

### Problematic
**Empathy** is missing in the virtual world
- Nowadays people are strongly connected but emotionally distant
- We looked at a more specific case of chat room

## Our Solution : CHATMO

### What is Chatmo ?
The assistant that processes anonymously each message, inferring what the users are feeling in real-time at a remarkable emotional depth. 

### Qualities
- Very portable and **reusable** piece of software, which can be virtually integrated everywhere.
- ChatMo is **privacy preserving**, contrary to other invasive techniques like facial recognition.

## Usage

##### You will need to create an API key for openAI to run our backend. [More infos here.](https://beta.openai.com/overview)
- In backend directory, create a file `config.py` and add a variable `openAI_API_key = "YOUR OPENAI API KEY"`

#### Local

##### Frontend
- From frontend directory, launch flutter with `flutter run -d chrome`
- It opens only 1 chrome window representing your first user. Do `Alt + D` and `Alt + Enter` to have your seconde user

##### Backend
- From backend directory, launch server with `python3 app.py`


## Example

|              Message 1               |              Message 2               |
| :----------------------------------: | :----------------------------------: |
| ![conversation 1](preview/Conv1.png) | ![conversation 2](preview/Conv2.png) |

|              Message 3               |              Message 4               |
| :----------------------------------: | :----------------------------------: |
| ![conversation 3](preview/Conv3.png) | ![conversation 4](preview/Conv4.png) |

Message 5 |
:-------------------------:|
![conversation 5](preview/Conv5.png)

## Improvements

- We used GIFs to represent user's emotion as they are more expressive than smileys. The main drawback is that GIF are always a bit funny and it is not necessarly what you want to express feelings such as sadness, anger, ... Our aim was to use Telegram's animated smileys.
- User's feeling that are shown on the conversation are fully decided by the IA. Users have no control over it. What we wanted to do is ask the user if the feeling decided by the IA represents well how he feels. 
- We could use user feedback to personalize our model and make it more accurate user-wise.
- If user A try to send profanitiesto user B, we could show a pop-up saying "Are you sure you want to send this message to B ?" .
- Extend the tool so it can be used in a group chat, not just a 1-to-1 conversation.
- In a group chat, if a user is beeing bullied, we could ask the bullied if he wants help and notify other participants to help him. 

## Midterm Report

### Text 2 Emotion
 
First, we began wit the very simple [Text2emotion](https://pypi.org/project/text2emotion/) package. Text2emotion is a python package which will help to extract  emotions from the content. Compatible with 5 different emotion categories as Happy, Angry, Sad, Surprise and Fear.

### Profanity Check
On top of Text2emotion, we added a profanity check with the [profanity-check](https://pypi.org/project/profanity-check/) library. profanity-check is a fast, robust python library to check for profanity or offensive language in strings.

### TextBlob
 We then added sentiment analysis with [TextBlob](https://textblob.readthedocs.io/en/dev/index.html) to improve our model. TextBlob is a simple library which supports complex analysis and operations on textual data. TextBlob return polarity and subjectivity of a sentence. Polarity lies between [-1, 1], where -1 indicates a negative sentiment and on the opposite, 1 defines a positive sentiment. Negation words reverse the polarity.
Subjectivity quantifies the amount of personal opinion and factual information contained in the text. The higher subjectivity means that the text contains personal opinion rather than factual information.

### TextBlob with Naive Bayes Analyzer
After that, we extended our TextBlob utilisation with the [Naive Bayes Analyzer](https://textblob.readthedocs.io/en/dev/advanced_usage.html). 

### Sentiment Intensity Analyzer 

Finally, we added a [Sentiment Intensity Analyzer](https://www.nltk.org/_modules/nltk/sentiment/vader.html#SentimentIntensityAnalyzer). NLTK already has a built-in, pretrained sentiment analyzer called VADER (Valence Aware Dictionary and sEntiment Reasoner).
Since VADER is pretrained, we could get results quicker than the other analyzers we used before. Also, VADER is best suited for language used in social media, like short senteces with some slang and abbreviations, which would also correspond to what we could find in a group chat.

Very useful notebook to 
[Compare sentiment analysis tools](https://colab.research.google.com/github/littlecolumns/ds4j-notebooks/blob/master/sentiment-analysis-is-bad/notebooks/Comparing%20sentiment%20analysis%20tools.ipynb) !

