from PyQt6.QtWidgets import *
from HumanInterfacing.SpeechToText import SpeechToText
from HumanInterfacing.TextToSpeech import TTSThread
from AI.ChatbotModel import Chatbot 

class ChatbotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.chatbot = Chatbot() 

        self.tts_engine = None

        self.stt_engine = SpeechToText()
        self.stt_engine.text_signal.connect(self.handle_chatbot_response)
        self.stt_engine.start()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # SET ALL BUTTONS AND TEXT EDITS
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
        self.setLayout(layout)

        self.load_styles()

    def load_styles(self):
        try:
            with open("Frontend/styles.qss", "r") as style_file:
                self.setStyleSheet(style_file.read())

        except FileNotFoundError:
            print("Warning: 'styles.qss' file not found.")


    def handle_user_input(self):
        user_message = self.user_input.text().strip()
        if not user_message:
            return

        # Get the user's name (default to "Anonymous")
        user_name = self.get_username()

        self.chat_display.append(f"{user_name}: {user_message}")
        self.user_input.clear()

        response = self.chatbot.get_response(user_message, user_name)
        self.chat_display.append(f"AI Receptionist: {response}")

        self.speak(response)

    def get_username(self):
        user_name, ok = QInputDialog.getText(self, "Username", "Enter your name (optional):")
        return user_name.strip() if ok and user_name else "Anonymous"

    def handle_chatbot_response(self, response):
        self.chat_display.append(f"AI Receptionist: {response}")
        self.speak(response)

    def start_listening(self):
        self.stt_engine.start()

    def speak(self, text, lang="en"):
        if self.tts_engine:
            self.tts_engine.quit()  # Stop any previous thread
            self.tts_engine.wait()

        self.tts_engine = TTSThread(text, lang)
        self.tts_engine.start()