from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer
from CameraModule.camera import Camera

class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.camera = Camera()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_picture)
        self.timer.start(30)

    def capture_picture(self):
        self.camera.get_frame()

    def closeEvent(self, event):
        self.camera.release()
        event.accept()
