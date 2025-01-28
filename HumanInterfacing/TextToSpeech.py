import pyttsx3
from PyQt6.QtCore import pyqtSignal ,QThread
class TTSThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 0.9)

    def run(self):
        self.engine.say(self.text)
        self.engine.runAndWait()
        self.finished_signal.emit()

    def speak(self, text):
        self.tts_thread = TTSThread(text)
        self.tts_thread.start()
