from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from Frontend.ChatbotWidget import ChatbotWidget

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Receptionist with Voice and Camera")
        self.setGeometry(100, 100, 1024, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Chatbot Widget ✅ Using updated chatbot widget
        chatbot_widget = ChatbotWidget()
        main_layout.addWidget(chatbot_widget)

        # Set main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
