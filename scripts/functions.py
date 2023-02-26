# -*- coding: utf-8 -*-
from libs import *
from possibility import *

def listen(stream, rec):
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']

def getDataFromJson(fileName):
    with open(fileName, "r", encoding="utf8") as jsonFile:
        return json.load(jsonFile)

def setDataToJson(fileName, file):
    with open(fileName, "w", encoding="utf8") as jsonFile:
        json.dump(file, jsonFile, sort_keys=False)

def startPythonFile(pathToFile):
    os.system(f"python {pathToFile}")

def say(message, CFLNFCS, err=None):
    if err != None:
        print("[ERROR]", err)
    else:
        print("Клара:", message)
    voise = gTTS(message, lang="ru")
    fvn = f"audio_{CFLNFCS['CountForLastNumberFromClaraSaids']}.mp3"
    CFLNFCS[0]['CountForLastNumberFromNODE'] += 1
    setDataToJson("bot_sys_data.json", CFLNFCS)
    voise.save(fvn)
    playsound.playsound(fvn)
    os.system(f"del {fvn}")

def smartSpeak(words, CFLNFCSdata):
    say(words[random.randint(0, len(words) - 1)], CFLNFCSdata)

def deleteAll(wordsForDeleting, value):
    for word in wordsForDeleting:
        value = value.replace(f"{word} ", "")
        value = value.replace(f" {word}", "")
        value = value.replace(f"{word}", "")
        return value

def listenedText():
    for text in listen():
        return text

def startAdaNN(botSYSDataFile, settingsDataFile,
            nowVar, monthVar, command=None,
            model_name="model.tflearn", intentsFile="intents.json"):
    AdaNN(botSYSDataFile, settingsDataFile,
            nowVar, monthVar, command=command,
            model_name=model_name, intentsFile=intentsFile)

def userIsHappy():
    cap = cv2.VideoCapture(0)
    smiles = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
    while True:
        success, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = smiles.detectMultiScale(gray, 1.4, 19)
        for (sx, sy, sw, sh) in result:
            return True
        else:
            return False
        cv2.waitKey(1)

def screenshot(numOfMonitor=0):
    with mss() as sc:
        sc.shot(mon=numOfMonitor)

def showDataTime(method, nowVar, monthVar):
    if method == "date":
        return f"Сегодня {nowVar.day}-ое {monthVar} {nowVar.year}-ого года"
    else:
        return f"А cейчас {str(nowVar.hour)}:{str(nowVar.minute)}"

def checkPossib(tag, nowVar, monthVar, botSYSDataFile):
    if tag == "turnOnCamera":
        startCv2(type="camera")
    if tag == "showIp":
        userIp = stun.get_ip_info()[1]
        print(userIp)
    if tag == "screenshot":
        screenshot()
    if tag == "showDate":
        say(showDataTime("date", nowVar, monthVar), botSYSDataFile)
    if tag == "showTime":
        say(showDataTime("time", nowVar, monthVar), botSYSDataFile)
    if tag == "turnOff":
        os.system("shutdown -s")
    if tag == "restartSYS":
        os.system("shutdown /r /t 1")
    if tag == "geolocation":
        webbrowser.open_new_tab(
            f"https://www.google.com.ua/maps/place/{geocoder.ip('me').latlng[0]},{geocoder.ip('me').latlng[1]}")
    if tag == "movementDetector":
        startCv2(type="md")