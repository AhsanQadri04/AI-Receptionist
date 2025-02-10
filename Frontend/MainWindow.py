from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from Frontend.ChatbotWidget import ChatbotWidget



class MainWindow(QMainWindow):
    """Main application window for the AI Receptionist with Voice and Camera."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Receptionist with Voice and Camera")
        self.setGeometry(100, 100, 1024, 600)
        self.initUI()

    def initUI(self):
        """Initializes the UI by creating and setting the main layout with the ChatbotWidget."""
        # Create a vertical layout for the main window.
        main_layout = QVBoxLayout()

        # Add the ChatbotWidget (which encapsulates the chatbot functionality) to the layout.
        chatbot_widget = ChatbotWidget()
        main_layout.addWidget(chatbot_widget)

        # Create a central widget, set its layout, and assign it as the central widget of the window.
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
