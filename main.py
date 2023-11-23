import os
import time
import pyaudio
import playsound
from gtts import gTTS
from openai import OpenAI
from pydantic import FilePath
import speech_recognition as sr
import pyautogui
import pytesseract
from PIL import Image


api_key = "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"
client = OpenAI(api_key = "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")


lang = 'en'
openai_api_key = api_key

guy = ""

microphone = sr.Microphone(device_index=1)



def play_audio(text):
    speech = gTTS(text=text, lang=lang, tld="com.au", slow=False)
    speech.save("audio.mp3")
    playsound.playsound("audio.mp3")
    os.remove("audio.mp3")

def create_note_file(file_path, note):
    with open(file_path, "a") as f:
        f.write(note + "\n")

def note_file(file_path, note):
    with open(file_path, "a") as f:
        f.write(note + "\n")

def get_audio():
    r = sr.Recognizer()
    with microphone as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
            global guy
            guy = said

            if "note" in said:
                print("Opening Note")
                play_audio("What would you like to make a note about")
                note_audio = r.listen(source)
                note = r.recognize_google(note_audio)
                print("Note Saved!")
                play_audio("Note was saved successfuly")
                file_path = os.path.expanduser("~/Desktop/note.txt")
                create_note_file(note, file_path)
            
            if "suck" in said:
                play_audio("I am sorry you are frustrated")

            elif "Friday" in said:
                new_string = said.replace("Friday", "")
                print(new_string)
                completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_string}])
                text = completion.choices[0].message.content
                play_audio(text)
                
        except Exception as e:
            print("Exception:", str(e))

while True:
    if "stop" in guy:
        break
    get_audio()