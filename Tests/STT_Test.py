from HumanInterfacing.SpeechToText import SpeechToText
import time

def test_speech_to_text():
    stt = SpeechToText()

    def print_text_output(text):
        print(f"Recognized Text: {text}")

    stt.text_signal.connect(print_text_output)
    stt.start()

    time.sleep(10)  # Allow testing for 10 seconds
    stt.stop()  # Stop the thread properly before exiting
    print("SpeechToText thread stopped.")

if __name__ == "__main__":
    test_speech_to_text()
