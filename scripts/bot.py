# -*- coding: utf-8 -*-
from libs import *
model = Model('model_for_speechR_s')
rec = KaldiRecognizer(model,16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True, frames_per_buffer=8000)
stream.start_stream()
sentiment = False
AAS_YEAH = "smartSpeak_YEAH"
def listen():
    while True:
        data = stream.read(4000,exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data)>0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']
def getDataFromJson(fileName):
    with open(fileName, "r", encoding="utf8") as jsonFile:
        return json.load(jsonFile)
def setDataToJson(fileName, file):
    with open(fileName, "w", encoding="utf-8") as jsonFile:
        json.dump(file, jsonFile, sort_keys=False)
settingsFile = getDataFromJson("setting.json")
botQueryData = getDataFromJson("bot_data.json")
botSYSData = getDataFromJson("bot_sys_data.json")
now = datetime.datetime.now()
month = botSYSData["monthClasses"][now.month-1]
def say(message, err=""):
    if err == "":
        print("Клара:",message)
    else:
        print("[ERROR]",message)
    voise = gTTS(message, lang="ru")
    fvn = "-audio-"+str(random.random())+".mp3"
    voise.save(fvn)
    playsound.playsound(fvn)
    os.system(f"del {fvn}")
def smartSpeak(words):
    say(words[random.randint(0,len(words)-1)])
def newYear():
    now = datetime.datetime.now()
    if now.month == 1 and now.day == 1:
        say(f"Привет, поздровляю тебя с новым {now.year}-ым")
    elif now.month == 12 and now.day == 31:
        say(f"Привет, с наступающим {now.year+1}-ым")
def deleteAll(wordsForDeleting,value):
    for word in wordsForDeleting:
        value = value.replace(f"{word} ","")
        value = value.replace(f" {word}","")
        value = value.replace(f"{word}", "")
        return value
def listenedText():
    for text in listen():
        return text
def mainDB_BOT(command = None, botQuetionDataJson, settingsDataFile, botSYSDataFile):
    for key in zip(list(botQuetionDataJson), botQuetionDataJson):
        if key in command:
            if botQuetionDataJson[key][1] == "sayYeah":
                smartSpeak(botSYSDataFile["smartSpeak_YEAH"])
            if botQuetionDataJson[key][2] == "deletable":
                cleanedCommand = deleteAll(botQuetionDataJson[key][3], command)
            if "writeList" in botQuetionDataJson[key][0]:
                valueForLoadingToFile = cleanedCommand
                with open(f"C:/post-{botSYSDataFile['CountForLastNumberFromNODE']}-.txt", "w", encoding="utf-8") as file:
                    file.write(valueForLoadingToFile)
                botSYSDataFile['CountForLastNumberFromNODE'] += 1
                setDataToJson("setting.json", botSYSDataFile)
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
                say(f"Сегодня {now.day}-ое {month} {now.year}-ого года")
            if "showTime" in botQuetionDataJson[key][0]:
                say(f"А cейчас {str(now.hour)}:{str(now.minute)}")
            else:
                smartSpeak(botQuetionDataJson[key][-1])
def userIsHappy():
    cap = cv2.VideoCapture(0)
    smiles = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_smile.xml")
    while True:
        success, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = smiles.detectMultiScale(gray, 1.4, 19)
        for (sx,sy,sw,sh) in result:
            return True
        else:
            return False
        cv2.waitKey(1)
main = Thread(target=mainDB_BOT, args=())
newyear = Thread(target=newYear, args=())
main.start()
newyear.start()
for text in listen():
    mainDB_BOT(text, settingsFile, botQueryData)
