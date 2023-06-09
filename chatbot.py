import random
import json
import pickle
import numpy as np

import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intent.json').read())


words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i,word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentece):
    bow = bag_of_words(sentece)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1],reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])})
    return return_list


while True:
    sentence = input()
    if sentence == "exit":
        break
    classe = predict_class(sentence)
    classe=classe[0]['intent']
    response = "I'm sorry, I don't understand. Could you please try again?"
    for intent in intents["intents"]:
        if intent["intent"] == classe:
            response = intent["responses"][0]
            break
    print(response)


