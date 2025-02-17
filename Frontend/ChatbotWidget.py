import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QInputDialog
from HumanInterfacing.SpeechToText import SpeechToText
from HumanInterfacing.TextToSpeech import TTSThread
from AI.ChatbotModel import Chatbot

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ChatbotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chatbot = Chatbot()
        self.tts_engine = None
        self.cached_username = None
        self.stt_engine = SpeechToText()
        self.stt_engine.text_signal.connect(self.handle_voice_input)
        self.stt_engine.start()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your message here...")
        input_layout.addWidget(self.user_input)
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.handle_user_input)
        input_layout.addWidget(send_button)
        voice_button = QPushButton("🎤 Speak")
        voice_button.clicked.connect(self.start_listening)
        input_layout.addWidget(voice_button)
        layout.addLayout(input_layout)
        self.load_styles()

    def load_styles(self):
        try:
            with open("Frontend/styles.qss", "r") as style_file:
                self.setStyleSheet(style_file.read())
        except FileNotFoundError:
            logging.warning("Warning: 'styles.qss' file not found.")

    def handle_user_input(self):
        user_message = self.user_input.text().strip()
        if not user_message:
            return
        user_name = self.get_username()
        self.chat_display.append(f"{user_name}: {user_message}")
        self.user_input.clear()
        response = self.chatbot.get_response(user_message, user_name)
        self.chat_display.append(f"AI Receptionist: {response}")
        self.speak(response)

    def get_username(self):
        if self.cached_username:
            return self.cached_username
        user_name, ok = QInputDialog.getText(self, "Username", "Enter your name (optional):")
        self.cached_username = user_name.strip() if ok and user_name else "Anonymous"
        return self.cached_username

    def handle_voice_input(self, recognized_text):
        self.chat_display.append(f"User (Voice): {recognized_text}")
        user_name = self.get_username()
        chatbot_response = self.chatbot.get_response(recognized_text, user_name)
        self.chat_display.append(f"AI Receptionist: {chatbot_response}")
        self.speak(chatbot_response)

    def start_listening(self):
        self.stt_engine.start()

    def speak(self, text, lang="en"):
        if self.tts_engine:
            self.tts_engine.quit()
            self.tts_engine.wait()
        self.tts_engine = TTSThread(text, lang)
        self.tts_engine.start()
