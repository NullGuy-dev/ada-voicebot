import functions as fn
import nltk
nltk.download('punkt')
import tflearn, tensorflow, random, json, pickle
import numpy as np
from nltk.stem.lancaster import LancasterStemmer
intentsFile = "intents.json"

stemmer = LancasterStemmer()
with open(intentsFile, encoding="utf8") as file:
    data = json.load(file)
with open("data.pickle","rb") as f:
    words,labels,training,output = pickle.load(f)

def AdaNN():
    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net,8)
    net = tflearn.fully_connected(net,8)
    net = tflearn.fully_connected(net,len(output[0]),activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    model.load("model.tflearn")
    return model

AdaNeuralNetwork = AdaNN()

def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

def chat(query, now, month, botSYSDataFile):
    results = AdaNeuralNetwork.predict([bag_of_words(query,words)])
    results_index = np.argmax(results)
    tag = labels[results_index]
    for tg in data["data"]:
        if tg['tag'] == tag:
            responses = tg['responses']
            fn.checkPossib(tg['tag'], now, month, botSYSDataFile)
    fn.printMethod(query)
    fn.say(random.choice(responses))