import sys
from PyQt6.QtWidgets import QApplication
from Frontend.MainWindow import mainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())
