# -*- coding: utf-8 -*-
import nltk
nltk.download('punkt')
import tflearn, tensorflow, random, json, pickle, keras
import numpy as np
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
intentsFile = "intents.json"
with open(intentsFile, encoding="utf8") as file:
    data = json.load(file)
try:
    with open("data.pickle","rb", encoding="utf8") as f:
        words,labels,training,output = pickle.load(f)
except:
    words = []
    labels = []
    classes = []
    docs_x = []
    docs_y = []

    for intent in data["data"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)
    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]
    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)
    with open("data.pickle","wb") as f:
        pickle.dump((words,labels,training,output),f)

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]),activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
v = int(input("v > "))
if v == 1:
    model.load("model.tflearn")
else:
    ephs = int(input("ephs > "))
    model.fit(training, output, n_epoch=ephs, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return np.array(bag)
def chat():
    while True:
        inp = input("> ")
        if inp.lower() == 'stop':
            break

        results = model.predict([bag_of_words(inp,words)])
        results_index = np.argmax(results)
        tag = labels[results_index]
        for tg in data["data"]:
            if tg['tag'] == tag:
                print(tg['tag'], results[0][results_index])
chat()
