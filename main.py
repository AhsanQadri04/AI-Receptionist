import os
# Set TensorFlow environment variable before importing any TensorFlow-related modules
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import sys
from PyQt6.QtWidgets import QApplication
from Frontend.MainWindow import MainWindow
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
