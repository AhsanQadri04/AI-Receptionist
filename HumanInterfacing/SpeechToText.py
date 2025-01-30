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

    def detect_spoken_language(self, audio):
        """Detects if the user is speaking in Urdu or English using Google STT."""
        try:
            recognized_text = self.recognizer.recognize_google(audio, language="ur")  # ✅ Try Urdu first
            print(f"🔹 Detected Spoken Language: Urdu")
            return recognized_text, "ur"
        except sr.UnknownValueError:
            try:
                recognized_text = self.recognizer.recognize_google(audio, language="en")  # ✅ Fallback to English
                print(f"🔹 Detected Spoken Language: English")
                return recognized_text, "en"
            except sr.UnknownValueError:
                print("❌ Speech Recognition could not understand the audio.")
                return None, None
        except sr.RequestError as e:
            print(f"❌ Speech Recognition API error: {e}")
            return None, None

    def run(self):
        print("SpeechToText thread started.")
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)  # ✅ Reduce background noise
                print("Microphone opened. Listening for audio...")
                
                while self.active:
                    try:
                        audio = self.recognizer.listen(source, timeout=5)
                        print("Audio captured. Sending to recognizer...")

                        recognized_text, detected_lang = self.detect_spoken_language(audio)
                        if recognized_text:
                            print(f"🔹 Recognized Text ({detected_lang}): {recognized_text}")
                            
                            # ✅ Chatbot ALWAYS responds in English
                            response = self.chatbot.get_response(recognized_text, detected_lang)
                            print(f"🤖 Chatbot Response (English): {response}")
                            
                            self.text_signal.emit(response)
                        else:
                            print("❌ No recognizable speech detected.")

                    except sr.RequestError as e:
                        print(f"❌ Speech Recognition API error: {e}")
                    except Exception as e:
                        print(f"❌ Unexpected error: {e}")

        except Exception as e:
            print(f"❌ Error initializing microphone: {e}")
        finally:
            print("SpeechToText thread finished.")
