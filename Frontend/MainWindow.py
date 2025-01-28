from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt

from HumanInterfacing.ChatbotWidget import ChatbotWidget
# from CameraModule.CameraWidget import CameraWidget

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Receptionist with Voice and Camera")
        self.setGeometry(100, 100, 1024, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Header
        header_label = self.create_header("Welcome to the AI Receptionist!")
        main_layout.addWidget(header_label)

        # Content Layout
        content_layout = self.create_content_layout()
        container = QWidget()
        container.setLayout(content_layout)
        main_layout.addWidget(container)

        # Set main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_header(self, text):
        header_label = QLabel(text)
        header_label.setStyleSheet("font-size: 20px; color: blue;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return header_label

    def create_content_layout(self):
        content_layout = QHBoxLayout()

        # Chatbot Widget
        chatbot_widget = ChatbotWidget(self)
        content_layout.addWidget(chatbot_widget)

        # Camera Widget
        # camera_widget = CameraWidget(self)
        # content_layout.addWidget(camera_widget)

        return content_layout

    # def closeEvent(self, event):
    #     self.findChild(CameraWidget).camera.release()  # Ensure the camera resource is released
    #     event.accept()