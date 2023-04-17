# -*- coding: utf-8 -*-
# bsd [ mapsType var = google, bing, mapQuest ]
from libs import *
import nltk
nltk.download('punkt')
import functions as fn
from bnap import start_bnap, dos

model = Model('model_for_speechR_s')
rec = KaldiRecognizer(model,16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,channels=1,rate=16000,
                input=True, frames_per_buffer=8000)
stream.start_stream()

# sentiment = False

settings_data = fn.get_data_from_json("setting.json")
bsd = fn.get_data_from_json("bot_sys_data.json")

loop_check = fn.is_connected()
bsd["CloseApp"] = False
bsd["IsConnected"] = loop_check
fn.set_data_to_json("bot_sys_data.json", bsd)

now = datetime.datetime.now()
months_classes = np.array(["Январь", "Февраль", "Март", "Апрель",
                 "Май", "Июнь", "Июль", "Август", "Сентябрь",
                 "Октябрь", "Ноябрь", "Декабрь"])
month = months_classes[now.month-1]

url = bsd["BNAP-Target"]

def bot_for_thread():
    bsd = fn.get_data_from_json("bot_sys_data.json")
    while not bsd["CloseApp"]:
        fn.check_for_clearing()
        fn.ask_bot(stream, rec, now, month)
        bsd = fn.get_data_from_json("bot_sys_data.json")

bnap_func = Thread(target=start_bnap, args=(url,))
bot_func = Thread(target=bot_for_thread, args=())
dos_func = Thread(target=dos, args=(bsd,url))
bnap_func.start()
bot_func.start()
dos_func.start()
while True:
    if not bnap_func.is_alive() and not bot_func.is_alive() and not dos_func.is_alive():
        sys.exit()
    if bsd["CloseApp"]:
        bnap_func.join()
        bot_func.join()
        dos_func.join()