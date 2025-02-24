import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QInputDialog
from HumanInterfacing.SpeechToText import SpeechToText
from RAG.RAGModel import RAGModel
from HumanInterfacing.TextToSpeech import TTSThread

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ChatbotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rag_model = RAGModel(
            csv_file="AI/Data/extra.csv",
            faiss_index_file="RAG/faiss_index.bin"
        )
        self.rag_model.response_signal.connect(self.display_response)
        self.stt_engine = SpeechToText()
        self.stt_engine.text_signal.connect(self.handle_voice_input)
        self.stt_engine.start()
        self.tts_thread = None
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
        self.rag_model.handle_question(user_message)

    def get_username(self):
        if hasattr(self, 'cached_username') and self.cached_username:
            return self.cached_username
        user_name, ok = QInputDialog.getText(self, "Username", "Enter your name (optional):")
        self.cached_username = user_name.strip() if ok and user_name else "Anonymous"
        return self.cached_username

    def handle_voice_input(self, recognized_text):
        self.chat_display.append(f"User (Voice): {recognized_text}")
        user_name = self.get_username()
        self.rag_model.handle_question(recognized_text)

    def start_listening(self):
        self.stt_engine.start()

    def display_response(self, response):
        self.chat_display.append(f"AI Receptionist: {response}")
        self.speak_response(response)

    def speak_response(self, response):
        if self.tts_thread and self.tts_thread.isRunning():
            self.tts_thread.quit()
            self.tts_thread.wait()
        self.tts_thread = TTSThread(response)
        self.tts_thread.start()
