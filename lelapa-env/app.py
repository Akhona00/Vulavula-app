import tkinter as tk
import random
from tkinter import messagebox
import random
from gtts import gTTS
import os
import requests
from PIL import Image, ImageTk
from playsound import playsound
from retry_requests import retry
from requests.adapters import HTTPAdapter
from requests import Session
from requests import Request
import qfrency

# Replace with your actual Vululua token
vulavula_token_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM1ZDk1NGU0MzMyMTQ4MzNhNzk0NmM5NmZkMTYyZTdkIiwiY2xpZW50X2lkIjo2NCwicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.1HchJDhAt2lYrK-dGdpVvDhx7S79DtL5VcFpI-9b7F4"

# Define the topics dictionary
topics = {
    "Biology": {
        "explanation": "Biology is the study of all living organisms (and dead organisms, like fossils). Biology looks at how these organisms form, develop and interact with each other and their environment. This includes all life; Humans, insects, plants, fungi, bacteria, anything that needs nutrients to survive.",
        "words": ["cell", "organism", "ecosystem", "photosynthesis"],
        "pictures" : [
             {"filename":"cell.jpeg"},
             {"filename": "lelapa-env/organism.jpeg"},
             {"filename": "C:/Vulavula app/lelapa-env/ecosystem.jpeg"},
             {"filename": "C:/Vulavula app/photosythesis.jpeg"}
        ]
    },
    "Chemistry": {
       "explanation": "Chemistry is the study of the properties, composition, and reactions of matter.",
        "words": ["atom", "molecule", "compound", "reaction"],
        "pictures": ["atom.png", "molecule.png", "compound.png", "reaction.png"]
    },

}

# Define your Qfrency Cloud API keys
X_ACCOUNT_KEY = "0b5091da-7a2b-476c-9b6d-517baa078ee8"
X_API_KEY = "263a08cc-4a1e-4f3c-aef9-69b1223fe668"

# Instantiate a Qfrency cloud API instance
cloud_api = qfrency.QfrencyCloudTTS(X_ACCOUNT_KEY, X_API_KEY)

def write_wav_to_file(wav, filename):
    p = open(filename, "wb")
    p.write(wav)
    p.close()

# Define a function to translate text using the Vululua API
def translate(text, language):
    if language == 'Zulu':
        
        payload = {
            "input_text" : text,
            "source_lang": "eng_Latn",
            "target_lang": "zul_Latn"
        }
    elif language == "Sesotho":
       

        payload = {
            "input_text" :  text,
            "source_lang": "eng_Latn",
            "target_lang": "sot_Latn"
        }
    else: 

        payload = {
            "input_text" : text,
            "source_lang": "eng_Latn",
            "target_lang": "engl_Latn"
        }
    url = "https://vulavula-services.lelapa.ai/api/v1/translate/process"
    headers = {
        "X-CLIENT-TOKEN": vulavula_token_key,
    }
    session = retry(Session(), retries=10, backoff_factor=1)


    translation_resp = session.post(
         url,
         json=payload,
         headers=headers,
    )

    return translation_resp.json()


# Define a function to convert text to speech
def text_to_speech(exp, language):
    voice_code = "eng_Latn"  # Default to English
    if language == "Zulu":
        voice_code = "zul_Latn"
    elif language == "Sesotho":
        voice_code = "sot_Latn"


    payload = {
        "exp": "An ecosystem is a community of living organisms (plants, animals and microbes) in a particular area. The term `eco' refers to a part of the world and `system' refers to the co-ordinating units. An ecosystem is a community of organisms and their physical environment interacting together.",
        "voice": voice_code
    }

    headers = {
        "X-Account-Key": "0b5091da-7a2b-476c-9b6d-517baa078ee8",
        "X-API-Key": "263a08cc-4a1e-4f3c-aef9-69b1223fe668",
        "Content-Type": "application/json"
    }

    # Send POST request to Qfrency API for TTS
    QFRENCY_API_URL = "https://tts.qfrency.com/api"
    response = requests.post(QFRENCY_API_URL, json=payload, headers=headers)
    
    wav_data = response.content
    synthed_wav_1 = cloud_api.synth(language,
                                exp)
    write_wav_to_file(synthed_wav_1, "synthed_wav_1.wav")   
 
   # Clean up the audio file after playing

# Define a function to start the game
def start_game(topic, language):
    explanation = topics[topic]["explanation"]
    translated_explanation = translate(explanation, language)
    explanation_label.config(text=translated_explanation)
    words = topics[topic]["words"]
    pictures = topics[topic]["pictures"]
    random.shuffle(pictures)
    for widget in words_frame.winfo_children():
        widget.destroy()
    for widget in pictures_frame.winfo_children():
        widget.destroy()
    for word in words:
        word_button = tk.Button(words_frame, text=word, command=lambda w=word: select_word(w))
        word_button.pack(side=tk.LEFT)
    for picture in pictures:
        img = Image.open(picture["filename"])
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        picture_button = tk.Button(pictures_frame, image=img, command=lambda p=picture: select_picture(p))
        picture_button.image = img
        picture_button.pack(side=tk.LEFT)
# Define global variables to keep track of selected word and picture
selected_word = None
selected_picture = None

def select_word(word):
    global selected_word
    selected_word = word
    check_match()

def select_picture(picture):
    global selected_picture
    selected_picture=picture
    play_audio_for_picture(picture)
    check_match()

def check_match():
    if selected_word and selected_picture:
        for topic, details in topics.items():
            if selected_word in details["words"] and selected_picture in details["pictures"]:
                if details["words"].index(selected_word) == details["pictures"].index(selected_picture):
                    result = "Correct!"
                    translated_word = translate(selected_word, language_var.get())
                    text_to_speech(translated_word, language_var.get())
                    explanation = details["explanation"]
                    translated_explanation = translate(explanation, language_var.get())
                    text_to_speech(translated_explanation, language_var.get())
                else:
                    result = "uxolo, akulungile!"
                result_label.config(text=result)
                break
        reset_selection()

def reset_selection():
    global selected_word, selected_picture
    selected_word = None
    selected_picture = None

def play_audio_for_picture(picture):
    topic = topic_var.get()
    for i, pic in enumerate(topics[topic]["pictures"]):
        if pic == picture:
            word = topics[topic]["exp"][i]
            text_to_speech(word, language_var.get())

# Create a Tkinter window
window = tk.Tk()
window.title("Language Game")

# Create a Tkinter frame for the game
frame = tk.Frame(window)
frame.pack()

# Create a Tkinter label to display the topic
topic_label = tk.Label(frame, text="Choose a topic:")
topic_label.pack()

# Create a Tkinter dropdown menu to select the topic
topic_var = tk.StringVar()
topic_menu = tk.OptionMenu(frame, topic_var, *topics.keys())
topic_menu.pack()

# Create a Tkinter label to display the language
language_label = tk.Label(frame, text="Choose a language:")
language_label.pack()

# Create a Tkinter dropdown menu to select the language
language_var = tk.StringVar()
language_menu = tk.OptionMenu(frame, language_var, "Zulu", "Sesotho")
language_menu.pack()

# Create a Tkinter button to start the game
start_button = tk.Button(frame, text="Start", command=lambda: start_game(topic_var.get(), language_var.get()))
start_button.pack()

# Create a Tkinter label to display the explanation
explanation_label = tk.Label(frame, text="", wraplength=400)
explanation_label.pack()

# Create frames to hold words and pictures
words_frame = tk.Frame(frame)
words_frame.pack()

pictures_frame = tk.Frame(frame)
pictures_frame.pack()

# Create a Tkinter label to display the result
result_label = tk.Label(frame, text="")
result_label.pack()

# Start the Tkinter event loop
window.mainloop() 

""" import tkinter as tk
from tkinter import messagebox
from gtts import gTTS
import os
import pygame
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# Replace with your actual Vululua token
vulavula_token_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM1ZDk1NGU0MzMyMTQ4MzNhNzk0NmM5NmZkMTYyZTdkIiwiY2xpZW50X2lkIjo2NCwicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.1HchJDhAt2lYrK-dGdpVvDhx7S79DtL5VcFpI-9b7F4"

class ScrimeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrime Game")
        self.language = None

        # Define the topics dictionary
        self.topics = {
            "Biology": {
                "explanation": "Biology is the study of living organisms and their interactions with each other and their environment.",
                "words": ["cell", "organism", "ecosystem", "evolution"],
                "pictures": ["cell.png", "organism.png", "ecosystem.png", "evolution.png"]
            },
            "Chemistry": {
                "explanation": "Chemistry is the study of the properties, composition, and reactions of matter.",
                "words": ["atom", "molecule", "compound", "reaction"],
                "pictures": ["atom.png", "molecule.png", "compound.png", "reaction.png"]
            },
            "Physics": {
                "explanation": "Physics is the study of the natural world around us, including energy, motion, and the behavior of matter and energy.",
                "words": ["energy", "motion", "force", "gravity"],
                "pictures": ["energy.png", "motion.png", "force.png", "gravity.png"]
            }
        }

        self.word_list = {
            'zulu': {'apple': 'i-apula', 'banana': 'ibhana', 'cat': 'ikati', 'dog': 'inja'},
            'sesotho': {'apple': 'apole', 'banana': 'banana', 'cat': 'katse', 'dog': 'ntja'}
        }
        self.images = ['apple.png', 'banana.png', 'cat.png', 'dog.png']
        self.words = []
        self.setup_ui()

    def setup_ui(self):
        # Language selection
        self.language_label = tk.Label(self.root, text="Choose language:")
        self.language_label.pack()

        self.language_var = tk.StringVar(value="zulu")
        self.zulu_rb = tk.Radiobutton(self.root, text="Zulu", variable=self.language_var, value="zulu")
        self.sesotho_rb = tk.Radiobutton(self.root, text="Sesotho", variable=self.language_var, value="sesotho")
        self.english_rb = tk.Radiobutton(self.root, text="English", variable=self.language_var, value="en")  # English added
        self.zulu_rb.pack()
        self.sesotho_rb.pack()
        self.english_rb.pack()

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        self.language = self.language_var.get()
        self.language_label.pack_forget()
        self.zulu_rb.pack_forget()
        self.sesotho_rb.pack_forget()
        self.english_rb.pack_forget()  # English radio button hidden
        self.start_button.pack_forget()

        self.load_game()

    def load_game(self):
        self.words = list(self.word_list[self.language].keys())
        self.display_images_and_words()

    def display_images_and_words(self):
        for idx, image in enumerate(self.images):
            img = tk.PhotoImage(file=image)
            img_label = tk.Label(self.root, image=img)
            img_label.image = img
            img_label.pack(side="left")

            word_label = tk.Label(self.root, text=self.words[idx])
            word_label.pack(side="left")
            word_label.bind("<Button-1>", lambda e, idx=idx: self.check_answer(idx))

    def check_answer(self, idx):
        selected_word = self.words[idx]
        correct_translation = self.word_list[self.language][selected_word]

        # Play audio explanation
        explanation_text = self.translate_text(f"{selected_word} in {self.language} is {correct_translation}", self.language)
        tts = gTTS(text=explanation_text, lang=self.language)
        tts.save("explanation.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("explanation.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def translate_text(self, text, language):
        url = "https://vulavula-services.lelapa.ai/api/v1/translate/process"
        headers = {
            "Authorization": f"Bearer {"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM1ZDk1NGU0MzMyMTQ4MzNhNzk0NmM5NmZkMTYyZTdkIiwiY2xpZW50X2lkIjo2NCwicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.1HchJDhAt2lYrK-dGdpVvDhx7S79DtL5VcFpI-9b7F4"}",
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "target_lang": language
        }

        # Setup retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        response = http.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get('translation', text)
        else:
            return text  # Fallback to original text if translation fails

if __name__ == "__main__":
    root = tk.Tk()
    game = ScrimeGame(root)
    root.mainloop()
 """