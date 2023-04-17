import os, json
with open("bot_sys_data.json", "r", encoding="utf8") as jsonFile:
    bsd = json.load(jsonFile)
os.system(f"""pip install pillow mss pyaudio mtranslate pyttsx3 pygame bs4 geocoder stun vosk
            clearai=={bsd['v-clearai']} tensorflow ipython nltk tflearn SpeechRecognition""")