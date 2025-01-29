import queue
import speech_recognition as sr
from PyQt6.QtCore import pyqtSignal, QThread
from AI.ChatbotModel import Chatbot

class SpeechToText(QThread):
    text_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.audio_queue = queue.Queue()
        self.active = True  # Track if thread is running
        self.chatbot = Chatbot()  # Initialize chatbot model
        print("SpeechToText initialized.")

    def stop(self):
        self.active = False
        self.quit()
        self.wait()

    def run(self):
        print("SpeechToText thread started.")
        try:
            with sr.Microphone() as source:
                print("Microphone opened. Listening for audio...")
                while self.active:
                    try:
                        audio = self.recognizer.listen(source, timeout=5)
                        print("Audio captured. Sending to recognizer...")

                        recognized_text = ""
                        detected_lang = "en"

                        try:
                            recognized_text = self.recognizer.recognize_google(audio, language="en")
                        except sr.UnknownValueError:
                            try:
                                recognized_text = self.recognizer.recognize_google(audio, language="ur")
                                detected_lang = "ur"
                            except sr.UnknownValueError:
                                print("Speech Recognition could not understand the audio.")
                                continue

                        print(f"Recognized text ({detected_lang}): {recognized_text}")
                        response = self.chatbot.get_response(recognized_text)  # FIXED: Only passing user_input
                        print(f"Chatbot Response: {response}")

                        self.text_signal.emit(response)

                    except sr.RequestError as e:
                        print(f"Speech Recognition API error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            print("SpeechToText thread finished.")
