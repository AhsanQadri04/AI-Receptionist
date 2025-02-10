import os
import pygame
import regex as re
import logging
import time

from PyQt6.QtCore import pyqtSignal, QThread
from gtts import gTTS
from langdetect import detect

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TTSThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, text, lang="en"):
        super().__init__()
        self.text = text
        self.lang = lang
        self.response_dir = "AI/Data/Responses/"
        os.makedirs(self.response_dir, exist_ok=True)  # Ensure directory exists
        logging.info("TTSThread initialized with text: '%s' and language: '%s'", self.text, self.lang)

    def run(self):
        """
        Executes the text-to-speech process:
          - Generates an MP3 file from text using gTTS.
          - Plays the MP3 file using pygame mixer.
          - Emits finished_signal when playback is complete.
        """
        try:
            output_path = os.path.join(self.response_dir, "response.mp3")
            
            # Reinitialize pygame mixer to ensure a clean state.
            pygame.mixer.quit()
            pygame.mixer.init()
            
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Generate TTS audio using gTTS.
            tts = gTTS(text=self.text, lang=self.lang, slow=False)
            tts.save(output_path)
            logging.info("TTS audio saved to '%s'", output_path)
            
            # Load and play the audio.
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()
            
            # Wait until playback finishes; use a small sleep to reduce CPU load.
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            self.finished_signal.emit()
            logging.info("Audio playback finished, finished_signal emitted.")
        
        except Exception as e:
            logging.error("Error in text-to-speech: %s", e)

    @staticmethod
    def detect_urdu(text):
        """
        Checks if the provided text contains Urdu script.
        
        Args:
            text (str): The text to check.
        
        Returns:
            bool: True if Urdu characters are detected, False otherwise.
        """
        urdu_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
        return bool(urdu_pattern.search(text))

    @staticmethod
    def speak(text):
        """
        Synchronously generates speech from text using gTTS and plays it using pygame.
        Automatically detects language using langdetect.
        
        Args:
            text (str): The text to speak.
        """
        try:
            # Automatically detect language and choose Urdu if applicable.
            lang_detected = detect(text)
            tts_lang = "ur" if lang_detected == "ur" else "en"
            
            temp_path = "response.mp3"
            tts = gTTS(text=text, lang=tts_lang)
            tts.save(temp_path)
            logging.info("TTS saved to '%s' with language '%s'", temp_path, tts_lang)
            
            pygame.mixer.init()
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Wait until the audio finishes playing.
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
        except Exception as e:
            logging.error("Error in Text-to-Speech: %s", e)
