from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from HumanInterfacing.SpeechToText import SpeechToText
from HumanInterfacing.TextToSpeech import TTSThread
from AI.ChatbotModel import Chatbot 

class ChatbotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize Chatbot
        self.chatbot = Chatbot() 

        # Initialize TTS Engine (Threaded)
        self.tts_engine = None

        # Initialize STT Engine
        self.stt_engine = SpeechToText()
        self.stt_engine.text_signal.connect(self.handle_chatbot_response)
        self.stt_engine.start()

        # Initialize UI
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Input layout
        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your message here...")
        input_layout.addWidget(self.user_input)

        # Send button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.handle_user_input)
        input_layout.addWidget(send_button)

        # Voice button
        voice_button = QPushButton("🎤 Speak")
        voice_button.clicked.connect(self.start_listening)
        input_layout.addWidget(voice_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

        # Apply styles
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

        self.chat_display.append(f"User: {user_message}")
        self.user_input.clear()

        # Get response from Chatbot ✅ Using new chatbot logic
        response = self.chatbot.get_response(user_message)
        self.chat_display.append(f"AI Receptionist: {response}")

        self.speak(response)

    def handle_chatbot_response(self, response):
        self.chat_display.append(f"AI Receptionist: {response}")
        self.speak(response)

    def start_listening(self):
        self.stt_engine.start()

    def speak(self, text):
        self.tts_engine = TTSThread(text)
        self.tts_engine.start()
