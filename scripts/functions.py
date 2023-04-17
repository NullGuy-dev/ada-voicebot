# -*- coding: utf-8 -*-
from libs import *
from possibility import *

tryTime = lambda time: f"0{str(time)}" if time < 10 else str(time)

get_date_time = lambda method, now_var, month_var: f"{now_var.day}-ое {month_var} {now_var.year}-ого года" if method == "date" else f"{tryTime(now_var.hour)}:{tryTime(now_var.minute)}"

def close_app():
    bsd = fn.get_data_from_json("bot_sys_data.json")
    bsd["CloseApp"] = True
    fn.set_data_to_json("bot_sys_data.json", bsd)

def restart_app():
    sp.call(['python', 'bot.py'])
    close_app()

def is_connected():
    try:
        requests.get('https://www.example.com/')
        return True
    except:
        return False

def print_method(text):
    print(text)

def vosk_method():
    for text in listen():
        return text

def sr_method():
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)
    with m as s:
        audio = r.listen(s)
    try:
        command = r.recognize_google(audio, language="ru-RU")
        return command.lower()
    except:
        return ""

def listen(stream, rec):
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']

def get_data_from_json(file_name):
    with open(file_name, "r", encoding="utf8") as json_file:
        return json.load(json_file)

def set_data_to_json(file_name, file):
    with open(file_name, "w", encoding="utf8") as json_file:
        json.dump(file, json_file, sort_keys=False)

def check_for_clearing():
    try:
        sp.call(['del', "audio.flac"])
    except:
        pass

def file_is_valid(file):
    for fname in os.listdir():
        if fname == file:
            return True
    return False

def say(message, err=None):
    if message != "":
        if err != None:
            print_method(f"[ERROR]: {err}")
        else:
            print_method(f"Ada: {message}")
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(message)
        engine.runAndWait()

# def user_is_happy():
#     cap = cv2.VideoCapture(0)
#     smiles = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
#     while True:
#         success, img = cap.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         result = smiles.detectMultiScale(gray, 1.4, 19)
#         for (sx, sy, sw, sh) in result:
#             return True
#         else:
#             return False
#         cv2.waitKey(1)

def screenshot(num_of_monitor=0):
    with mss() as sc:
        sc.shot(mon=num_of_monitor)

def gpt(command):
    openai.api_key = "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"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=command,
        max_tokens=1024,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.1,
        presence_penalty=0.0
    )
    filthy_answer = response["choices"][0]["text"]
    fa_indx = filthy_answer.find("\n")
    answer = filthy_answer.replace(filthy_answer[:fa_indx:], "").lstrip("\n")
    return answer

def translator():
    bsd = fn.get_data_from_json("bot_sys_data.json")
    text = bsd["translate_data"]["TextForTranslating"]
    translated_text = translate(text, bsd["translate_data"]["TranslatedLangText"][0])
    bsd["translate_data"]["TextForTranslating"][1] = translated_text

def check_possib(tag, now_var, month_var): # тут подключение к функциям, согласно тегу
    # ДЛЯ QA: ты запрашиваешь каждый из этих методов, любыми словами!
    # Часть функций не готовы для бота, поэтому бот просто выводит ихние названия в консоль
    if tag == "camera":
        ClearAI.startCv2(type="camera")
    elif tag == "showIP":
        userIp = stun.get_ip_info()[1]
        print_method(userIp)
    elif tag == "screenshot":
        screenshot()
    elif tag == "date":
        say(get_date_time("date", now_var, month_var))
    elif tag == "time":
        say(get_date_time("time", now_var, month_var))
    elif tag == "turnOff":
        print_method("Отключения")
        # os.system("shutdown -s")
    elif tag == "restart":
        print_method("Перезагрузка")
        # os.system("shutdown /r /t 1")
    elif tag == "geolocation":
        coordn = np.array([])
        try:
            gpsd.connect()
            packet = gpsd.get_current()
            if packet.mode >= 2:
                latitude, longitude = packet.position()
                coordn = np.append(coordn, [latitude, longitude])
            else:
                print_method("Ошибка при получении данных о местоположении через GPS")
        except:
            coordn = np.array([geocoder.ip('me').latlng[0], geocoder.ip('me').latlng[1]])
        webbrowser.open_new_tab(
            f"https://www.google.com.ua/maps/place/{coordn[0]},{coordn[1]}")
    elif tag == "movementDetection":
        ClearAI.startCv2(type="md")
    elif tag == "translate":
        # translator()
        # эта функция не совсем готова!
        print("Переводчик")
    elif tag == "wf":
        print("Прогноз погоды")
    elif tag == "reminder":
        print("Напоминалка")
    elif tag == "bitcoinF":
        print("Прогноз курсабиткоина")
    elif tag == "ethereumF":
        print("Прогноз курса эфириума")
    elif tag == "akinator":
        print("Акинатор")
    elif tag == "HS":
        print("HS")
    elif tag == "convert":
        print("Конвертер изображений")

def vosk_ask_type(stream, rec, now, month):
    print_method("\n\n\n\n\nVOSK\n\n\n\n\n")
    for text in listen(stream, rec):
        bsd = fn.get_data_from_json("bot_sys_data.json")
        if bsd["CloseApp"]:
            break
        chat(now, month, text.lower())

def speech_recognition_ask_type(bsd, stream, rec, now, month):
    print_method("\n\n\n\n\nSpeech_recognition\n\n\n\n\n")
    while not bsd["CloseApp"]:
        chat(now, month, sr_method())
        bsd = fn.get_data_from_json("bot_sys_data.json")

def ask_bot(stream, rec, now, month):
    bsd = fn.get_data_from_json("bot_sys_data.json")
    if bsd["speechModelType"] == "auto": # если значение speechModelType в файле bot_sys_data.json будет - auto. auto - это значение которое означает что если у пользователя нет проблем с интернетом, тогда использовать модель speech_recognition, а если проблемы присутствуют, тогда использовать vosk
        if not is_connected():
            vosk_ask_type(stream, rec, now, month)
        elif is_connected():
            speech_recognition_ask_type(bsd, stream, rec, now, month)
    elif bsd["speechModelType"] == "speech_recognition": # это просто использование speech_recognition, даже если нет подключения к инету(speech_recognition не будет работать)
        speech_recognition_ask_type(bsd, stream, rec, now, month)
    elif bsd["speechModelType"] == "vosk": # это значит что будет использовать только vosk
        vosk_ask_type(stream, rec, now, month)
