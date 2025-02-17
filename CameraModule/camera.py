import cv2
import os
import time

output_folder = os.path.join(os.path.dirname(__file__), "Entry")
os.makedirs(output_folder, exist_ok=True)

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.face_counter = 0
        self.last_capture_time = 0
        self.person_detected = False
        self.image_captured = False

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret or frame is None:
            return None, False

        faces = self._detect_faces(frame)
        face_detected_now = bool(faces)

        if face_detected_now:
            self._handle_face_detected(frame)
        else:
            self._reset_detection_state()

        return frame, face_detected_now

    def _detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return faces

    def _handle_face_detected(self, frame):
        if not self.person_detected:
            self.person_detected = True
            self.image_captured = False
            self.last_capture_time = time.time()
        elif time.time() - self.last_capture_time >= 2 and not self.image_captured:
            self.capture_image(frame)

    def _reset_detection_state(self):
        self.person_detected = False
        self.image_captured = False

    def capture_image(self, frame):
        self.face_counter += 1
        image_path = os.path.join(output_folder, f'face_{self.face_counter}.jpg')
        cv2.imwrite(image_path, frame)
        print(f"Image saved at: {image_path}")
        self.image_captured = True

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
