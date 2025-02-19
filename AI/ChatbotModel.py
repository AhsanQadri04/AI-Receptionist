import time
import os
import logging
from fuzzywuzzy import process
from spellchecker import SpellChecker
from datetime import datetime
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from AI.developer_override import developer_override
from CameraModule.camera import Camera
from AI.Modules.JsonProcessing import load_json, save_json
from AI.Modules.textProcessing import preprocess_text, get_intent
from AI.Modules.queryHandler import handle_department_query
from AI.Modules.learningModule import reinforce_learning

DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
logging.basicConfig(filename="AI/Data/chatbot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Chatbot:
    def __init__(self, intent_file="AI/Data/intent.json", context_file="AI/Data/context.json"):
        self.intent_file = intent_file
        self.context_file = context_file
        self.data = load_json(intent_file, default_data={"intents": []})
        self.context = load_json(context_file, default_data={"logs": []})
        self.last_input_time = time.time()
        self.user_name = None
        self.camera = Camera()
        self.spell = SpellChecker()
        self.vectorizer = TfidfVectorizer()
        self.intent_patterns = [
            preprocess_text(pattern)
            for intent in self.data.get("intents", [])
            for pattern in intent.get("patterns", [])
            if isinstance(pattern, str)
        ]
        if self.intent_patterns:
            self.X = self.vectorizer.fit_transform(self.intent_patterns)
        else:
            logging.warning("No intent patterns found for TF-IDF training.")
            self.X = None

    def capture_face(self):
        _, frame = self.camera.get_frame()
        if frame is not None:
            image_path = self.camera.capture_image(frame)
            self.camera.release()
            return image_path
        logging.info("No face detected during capture.")
        return None

    def fuzzy_match(self, user_input):
        best_match = None
        best_score = 0
        for intent in self.data.get("intents", []):
            for pattern in intent.get("patterns", []):
                score = process.extractOne(user_input, [pattern])[1]
                if score > best_score:
                    best_score = score
                    best_match = intent
        return best_match if best_score >= 80 else None

    def correct_spelling(self, text):
        return ' '.join([self.spell.correction(word) if self.spell.correction(word) else word for word in text.split()])

    def get_response(self, user_input, user_name=None):
        user_input = self.correct_spelling(user_input)
        intent = self.fuzzy_match(user_input)
        response = "I'm sorry, I didn't understand. Could you rephrase?"
        if intent:
            if intent.get("tag") == "office_location":
                response = handle_department_query(user_input, self.data, self.intent_file)
            elif intent.get("responses"):
                response = intent["responses"][0]
        if DEBUG_MODE:
            response = developer_override(user_input, response, self.data, self.intent_file, self.context_file)
            logging.debug("Developer override applied to response.")
        return response

    def log_interaction(self, user_input, response, face_path):
        log_entry = {
            "face_image": face_path if face_path else "No Face Detected",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": user_input,
            "answer": response
        }
        self.context.setdefault("logs", []).append(log_entry)
        save_json(self.context_file, self.context)
        reinforce_learning(user_input, response, self.data, self.intent_file)
        logging.info(f"Logged interaction: {log_entry}")

    def preprocess_text(text):
        if isinstance(text, str):
            words = word_tokenize(text.lower())
            return " ".join(words)
        else:
            return ""
