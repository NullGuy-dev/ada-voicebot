# -*- coding: utf-8 -*-
from libs import *
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

def newYear(nowVar):
    if nowVar.month == 1 and nowVar.day == 1:
        say(f"Привет, поздровляю тебя с новым {nowVar.year}-ым")
    elif nowVar.month == 12 and nowVar.day == 31:
        say(f"Привет, с наступающим {nowVar.year + 1}-ым")

def deleteAll(wordsForDeleting, value):
    for word in wordsForDeleting:
        value = value.replace(f"{word} ", "")
        value = value.replace(f" {word}", "")
        value = value.replace(f"{word}", "")
        return value

def listenedText():
    for text in listen():
        return text

def mainDB_BOT(dataForSAYYN, botQuetionDataJson, settingsDataFile, botSYSDataFile, nowVar, monthVar, command=None):
    for key in list(botQuetionDataJson):
        if key in command:
            if botQuetionDataJson[key][1] == "sayYeah":
                smartSpeak(botSYSDataFile[dataForSAYYN[0]])
            if botQuetionDataJson[key][1] == "sayNope":
                smartSpeak(botSYSDataFile[dataForSAYYN[1]])
            if botQuetionDataJson[key][2] == "deletable":
                listForClean = botQuetionDataJson[key][3] + botSYSDataFile["listForDeletingBotNameFromQuetion"]
                cleanedCommand = deleteAll(listForClean, command)
            if "writeList" in botQuetionDataJson[key][0]:
                valueForLoadingToFile = cleanedCommand
                with open(f"E:/Programming/note_{botSYSDataFile['CountForLastNumberFromNODE']}.txt", "w",
                          encoding="utf8") as file:
                    file.write(valueForLoadingToFile)
                botSYSDataFile['CountForLastNumberFromNODE'] += 1
                setDataToJson("bot_sys_data.json", botSYSDataFile)
            if "turnOnCamera" in botQuetionDataJson[key][0]:
                cap = cv2.VideoCapture(0)
                while cap.isOpened():
                    success, img = cap.read()
                    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    cv2.imshow("Camera", img)
                    if cv2.waitKey(1) & 0xff == ord('x'):
                        break
                cap.release()
                cv2.destroyAllWindows()
            if botQuetionDataJson[key][0] == "showIp":
                print(stun.get_ip_info()[1])
                say(stun.get_ip_info()[1])
            if "ScreenShot" in botQuetionDataJson[key][0]:
                with mss() as sc:
                    sc.shot(mon=0)
            if "showDate" in botQuetionDataJson[key][0]:
                say(f"Сегодня {nowVar.day}-ое {monthVar} {nowVar.year}-ого года", botSYSDataFile)
            if "showTime" in botQuetionDataJson[key][0]:
                say(f"А cейчас {str(nowVar.hour)}:{str(nowVar.minute)}", botSYSDataFile)
            if botQuetionDataJson[key][-1] != "":
                smartSpeak(botQuetionDataJson[key][-1], botSYSDataFile)
    newYear(nowVar)

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
