import os
import pygame
from gtts import gTTS
from PyQt6.QtCore import pyqtSignal, QThread

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

            # Stop and uninitialize pygame if already running
            pygame.mixer.quit()  
            pygame.mixer.init()

            # Delete previous response file if it exists
            if os.path.exists(output_path):
                os.remove(output_path)

            # Generate speech using gTTS
            tts = gTTS(text=self.text, lang=self.lang, slow=False)
            tts.save(output_path)

            # Reload and play the generated speech
            pygame.mixer.init()
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.delay(100)  # Prevent infinite loop freeze

            self.finished_signal.emit()

        except Exception as e:
            print(f"Error in text-to-speech: {e}")

    def speak(self, text, lang="en"):
        self.tts_thread = TTSThread(text, lang)
        self.tts_thread.start()
