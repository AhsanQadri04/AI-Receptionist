import os
import pygame
import regex as re

from PyQt6.QtCore import pyqtSignal, QThread
from gtts import gTTS
from langdetect import detect

class TTSThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, text, lang="en"):
        super().__init__()
        self.text = text
        self.lang = lang
        self.response_dir = "AI/Data/Responses/"
        os.makedirs(self.response_dir, exist_ok=True)  # Ensure directory exists

    def run(self):
        try:
            output_path = os.path.join(self.response_dir, "response.mp3")

            pygame.mixer.quit()  
            pygame.mixer.init()

            if os.path.exists(output_path):
                os.remove(output_path)

            tts = gTTS(text=self.text, lang=self.lang, slow=False)
            tts.save(output_path)

            pygame.mixer.init()
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.delay(100)  # Prevent infinite loop freeze

            self.finished_signal.emit()

        except Exception as e:
            print(f"Error in text-to-speech: {e}")

    def detect_urdu(text):
        urdu_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')  # ✅ Unicode range for Urdu script
        return bool(urdu_pattern.search(text))

    def speak(text):
        try:
            lang = detect(text)  
            tts_lang = "ur" if lang == "ur" else "en"

            tts = gTTS(text=text, lang=tts_lang)
            tts.save("response.mp3")

            pygame.mixer.init()
            pygame.mixer.music.load("response.mp3")
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                continue
            
        except Exception as e:
            print(f"❌ Error in Text-to-Speech: {e}")