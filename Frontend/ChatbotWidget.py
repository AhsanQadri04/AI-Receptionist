import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QInputDialog
from HumanInterfacing.SpeechToText import SpeechToText
from HumanInterfacing.TextToSpeech import TTSThread
from AI.ChatbotModel import Chatbot

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ChatbotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize the chatbot and multimedia engines.
        self.chatbot = Chatbot()
        self.tts_engine = None
        
        # Optionally cache the username to avoid repeated prompts.
        self.cached_username = None
        
        self.stt_engine = SpeechToText()
        self.stt_engine.text_signal.connect(self.handle_chatbot_response)
        self.stt_engine.start()
        
        self.initUI()

    def initUI(self):
        # Create the main vertical layout.
        layout = QVBoxLayout(self)
        
        # Chat display: Read-only text edit.
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Input area: a horizontal layout with a QLineEdit and buttons.
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
        
        # Apply a stylesheet if available.
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
        
        # Retrieve or prompt for username only once.
        user_name = self.get_username()
        
        # Append user's message to the chat display.
        self.chat_display.append(f"{user_name}: {user_message}")
        self.user_input.clear()
        
        # Get chatbot response. Note: The second parameter here is used
        # to provide context (user's name), which your Chatbot.get_response()
        # method may use.
        response = self.chatbot.get_response(user_message, user_name)
        self.chat_display.append(f"AI Receptionist: {response}")
        
        self.speak(response)

    def get_username(self):
        # Cache the username after the first prompt.
        if self.cached_username:
            return self.cached_username
        
        user_name, ok = QInputDialog.getText(self, "Username", "Enter your name (optional):")
        self.cached_username = user_name.strip() if ok and user_name else "Anonymous"
        return self.cached_username

    def handle_chatbot_response(self, response):
        # This slot is connected to the STT engine's text_signal.
        self.chat_display.append(f"AI Receptionist: {response}")
        self.speak(response)

    def start_listening(self):
        # Restart the speech-to-text engine when the voice button is clicked.
        self.stt_engine.start()

    def speak(self, text, lang="en"):
        # If a previous TTS thread is running, quit it and wait for it to finish.
        if self.tts_engine:
            self.tts_engine.quit()
            self.tts_engine.wait()
        
        # Create and start a new text-to-speech thread.
        self.tts_engine = TTSThread(text, lang)
        self.tts_engine.start()
