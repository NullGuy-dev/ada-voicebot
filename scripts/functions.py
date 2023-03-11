# -*- coding: utf-8 -*-
from libs import *
from possibility import *

def restartApp():
    sp.call(['python', 'bot.py'])
    sys.exit()

def isConnected():
    try:
        requests.get('https://www.google.com/')
        return True
    except:
        return False

def printMethod(text):
    print(text)

def voskMethod():
    for text in listen():
        return text

def srMethod():
    r = sr.Recognizer()
    m = sr.Microphone(device_index=3)
    with m as s:
        audio = r.listen(s)
    try:
        command = r.recognize_google(audio, language="ru-RU")
        return command.lower()
    except:
        restartApp()

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

def say(message, err=None):
    if message != "":
        if err != None:
            print("[ERROR]", err)
        else:
            print("Ada:", message)
        CFLNFCS = getDataFromJson("bot_sys_data.json")
        voise = gTTS(message, lang="ru")
        os.system(f"del audio_{CFLNFCS['CountForLastNumberFromAdaWords']}.mp3")
        CFLNFCS['CountForLastNumberFromAdaWords'] += 1
        fvn = f"audio_{CFLNFCS['CountForLastNumberFromAdaWords']}.mp3"
        setDataToJson("bot_sys_data.json", CFLNFCS)
        voise.save(fvn)
        playsound.playsound(fvn)

def smartSpeak(words, CFLNFCSdata):
    say(words[random.randint(0, len(words) - 1)], CFLNFCSdata)

def deleteAll(wordsForDeleting, value):
    for word in wordsForDeleting:
        value = value.replace(f"{word} ", "")
        value = value.replace(f" {word}", "")
        value = value.replace(f"{word}", "")
        return value

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

def threadCheckIsConnected():
    botSysData = getDataFromJson("bot_sys_data.json")
    if botSysData["IsConnected"] != isConnected():
        botSysData["IsConnected"] = isConnected()
        setDataToJson("bot_sys_data.json", botSysData)
        restartApp()

def startBot(stream, rec, now, month, botSYSDataFile):
    if not isConnected():
        printMethod("\n\n\n\n\nVOSK\n\n\n\n\n")
        for text in listen(stream,rec):
            chat(text.lower(), now, month, botSYSDataFile)
    elif isConnected():
        printMethod("\n\n\n\n\nSpeech_recognition\n\n\n\n\n")
        while True:
            chat(srMethod(), now, month, botSYSDataFile)