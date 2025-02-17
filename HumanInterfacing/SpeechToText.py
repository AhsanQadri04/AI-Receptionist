import speech_recognition as sr
import logging
from PyQt6.QtCore import pyqtSignal, QObject, QThread

class SpeechToText(QThread):
    text_signal = pyqtSignal(str)

    def __init__(self):
        super(SpeechToText, self).__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        logging.info("SpeechToText initialized.")

    def run(self):
        self.start_listening()

    def start_listening(self):
        with self.microphone as source:
            logging.info("Microphone opened. Listening for audio...")
            audio = self.recognizer.listen(source)
            logging.info("Audio captured. Sending to recognizer...")

            try:
                # Recognize speech using Google Speech Recognition (English only)
                text = self.recognizer.recognize_google(audio, language='en-US')
                logging.info(f"Recognized Text: {text}")
                self.text_signal.emit(text)
                return text
            except sr.UnknownValueError:
                logging.error("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                logging.error(f"Could not request results from Google Speech Recognition service; {e}")

        return None