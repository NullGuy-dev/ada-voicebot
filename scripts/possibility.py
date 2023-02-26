from libs import *
from functions import *

def bag_of_words(s, words, stemmer):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

def chat(model, data, labels, inp, words, nowVar, monthVar, botSYSDataFile):
    while True:
        results = model.predict([bag_of_words(inp, words)])
        results_index = np.argmax(results)
        tag = labels[results_index]
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                checkPossib(tg['tag'], nowVar, monthVar, botSYSDataFile)
        say(random.choice(responses))

def AdaNN(botSYSDataFile, settingsDataFile,
            nowVar, monthVar, command=None,
            model_name="model.tflearn", intentsFile="intents.json"):
    stemmer = LancasterStemmer()
    words = []
    labels = []
    classes = []
    docs_x = []
    docs_y = []
    with open(intentsFile) as file:
        data = json.load(file)
    try:
        with open("data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)
    except:
        for intent in data["intents"]:
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
        with open("data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)
    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)
    model = tflearn.DNN(net)
    try:
        model.load(model_name)
    except:
        model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
        model.save(model_name)
    chat(model, data, labels, command, words, nowVar, monthVar, botSYSDataFile)