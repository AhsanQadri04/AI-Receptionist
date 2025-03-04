import os
import pygame
import logging
import time
from PyQt6.QtCore import pyqtSignal, QThread
from gtts import gTTS  # Import gTTS module

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TTSThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, text, lang="en"):
        super().__init__()
        self.text = text
        self.lang = lang
        self.response_dir = "AI/Data/Responses/"
        os.makedirs(self.response_dir, exist_ok=True)
        logging.info("TTSThread initialized with text: '%s' and language: '%s'", self.text, self.lang)

    def run(self):
        try:
            output_path = os.path.join(self.response_dir, "response.mp3")
            self._initialize_pygame()
            self._remove_existing_file(output_path)
            self._generate_tts_audio(output_path)
            self._play_audio(output_path)
            self.finished_signal.emit()
            logging.info("Audio playback finished, finished_signal emitted.")
        except Exception as e:
            logging.error("Error in text-to-speech: %s", e)

    def _initialize_pygame(self):
        pygame.mixer.quit()
        pygame.mixer.init()

    def _remove_existing_file(self, path):
        if os.path.exists(path):
            os.remove(path)

    def _generate_tts_audio(self, path):
        tts = gTTS(text=self.text, lang=self.lang, slow=False)
        tts.save(path)
        logging.info("TTS audio saved to '%s'", path)

    def _play_audio(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    @staticmethod
    def speak(text):
        try:
            temp_path = "response.mp3"
            tts = gTTS(text=text, lang="en")
            tts.save(temp_path)
            logging.info("TTS saved to '%s' with language 'en'", temp_path)
            pygame.mixer.init()
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            logging.error("Error in Text-to-Speech: %s", e)
