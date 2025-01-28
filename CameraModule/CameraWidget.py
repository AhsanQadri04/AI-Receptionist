from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer
from CameraModule.camera import Camera


class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize the Camera
        self.camera = Camera()

        # Timer to handle the frame processing and image capture
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_picture)
        self.timer.start(30)  # 30ms intervals

    def capture_picture(self):
        """
        Call the camera logic to process frames and capture images based on detection.
        """
        _, _ = self.camera.get_frame()  # Logic is already handled in camera.py

    def closeEvent(self, event):
        """
        Release the camera resource on window close.
        """
        self.camera.release()
        event.accept()
