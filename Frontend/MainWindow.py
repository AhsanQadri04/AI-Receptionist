from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from Frontend.ChatbotWidget import ChatbotWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Receptionist with Voice and Camera")
        self.setGeometry(100, 100, 1024, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        chatbot_widget = ChatbotWidget()
        main_layout.addWidget(chatbot_widget)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
