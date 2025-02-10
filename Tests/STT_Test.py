import sys
import time
from PyQt6.QtCore import QCoreApplication, QTimer
from HumanInterfacing.SpeechToText import SpeechToText

def test_speech_to_text():
    app = QCoreApplication(sys.argv)
    stt = SpeechToText()

    def print_text_output(text):
        print(f"Recognized Text: {text}")

    stt.text_signal.connect(print_text_output)
    stt.start()

    # Stop the STT thread after 10 seconds and quit the app.
    QTimer.singleShot(10000, lambda: (stt.stop(), app.quit()))
    app.exec()
    print("SpeechToText thread stopped.")

if __name__ == "__main__":
    test_speech_to_text()
