import queue  # Note: currently unused, remove if not needed.
import speech_recognition as sr
import logging

from PyQt6.QtCore import pyqtSignal, QThread
from AI.ChatbotModel import Chatbot

class SpeechToText(QThread):
    """
    A QThread-based speech-to-text engine that listens to audio from the microphone,
    detects whether the spoken language is Urdu or English, obtains a chatbot response,
    and emits the response via the text_signal.
    """
    text_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        # Unused audio_queue: remove if not needed in the future.
        self.audio_queue = queue.Queue()
        self.active = True  # Controls the running state of the thread.
        self.chatbot = Chatbot()  # Initialize the chatbot model.
        logging.info("SpeechToText initialized.")

    def stop(self):
        """Stops the SpeechToText thread gracefully."""
        self.active = False
        self.quit()
        self.wait()
        logging.info("SpeechToText thread stopped.")

    def detect_spoken_language(self, audio):
        """
        Attempts to recognize the spoken text in the given audio using Google Speech Recognition.
        First tries Urdu; if unsuccessful, falls back to English.
        
        Returns:
            tuple: (recognized_text, language_code) if successful, or (None, None) on failure.
        """
        try:
            recognized_text = self.recognizer.recognize_google(audio, language="ur")  # Try Urdu first.
            logging.info("Detected Spoken Language: Urdu")
            return recognized_text, "ur"
        except sr.UnknownValueError:
            try:
                recognized_text = self.recognizer.recognize_google(audio, language="en")  # Fallback to English.
                logging.info("Detected Spoken Language: English")
                return recognized_text, "en"
            except sr.UnknownValueError:
                logging.error("Speech Recognition could not understand the audio.")
                return None, None
        except sr.RequestError as e:
            logging.error(f"Speech Recognition API error: {e}")
            return None, None

    def run(self):
        """Main thread loop that continuously listens for audio and processes it."""
        logging.info("SpeechToText thread started.")
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)  # Reduce background noise.
                logging.info("Microphone opened. Listening for audio...")
                while self.active:
                    try:
                        # Listen for audio; timeout after 5 seconds if nothing is heard.
                        audio = self.recognizer.listen(source, timeout=5)
                        logging.info("Audio captured. Sending to recognizer...")

                        recognized_text, detected_lang = self.detect_spoken_language(audio)
                        if recognized_text:
                            logging.info(f"Recognized Text ({detected_lang}): {recognized_text}")
                            
                            # The chatbot is expected to respond in English.
                            response = self.chatbot.get_response(recognized_text, detected_lang)
                            logging.info(f"Chatbot Response (English): {response}")
                            
                            self.text_signal.emit(response)
                        else:
                            logging.warning("No recognizable speech detected.")
                    except sr.WaitTimeoutError:
                        logging.warning("Listening timed out while waiting for speech.")
                    except sr.RequestError as e:
                        logging.error(f"Speech Recognition API error during listen: {e}")
                    except Exception as e:
                        logging.error(f"Unexpected error: {e}")
        except Exception as e:
            logging.error(f"Error initializing microphone: {e}")
        finally:
            logging.info("SpeechToText thread finished.")
