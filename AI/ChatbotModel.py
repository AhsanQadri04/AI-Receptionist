# GENERAL IMPORTS
import time
import os
import logging

# SPECIFIC IMPORTS
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from AI.developer_override import developer_override
from CameraModule.camera import Camera

# MODULE IMPORTS
from AI.Modules.JsonProcessing import load_json, save_json
from AI.Modules.textProcessing import preprocess_text, get_intent
from AI.Modules.queryHandler import handle_department_query
from AI.Modules.learningModule import reinforce_learning
from AI.Modules.Translation import MachineTranslation

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "false" 

# Setup logging
logging.basicConfig(filename="AI/Data/chatbot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class Chatbot:
    def __init__(self, intent_file="AI/Data/intent.json", context_file="AI/Data/context.json"):
        self.intent_file = intent_file
        self.context_file = context_file
        self.data = load_json(intent_file, default_data={"intents": []})
        self.context = load_json(context_file, default_data={"logs": []})
        self.last_input_time = time.time()
        self.user_name = None
        self.camera = Camera()
        self.translator = MachineTranslation()

        # Train TF-IDF model
        self.vectorizer = TfidfVectorizer()
        self.intent_patterns = [preprocess_text(pattern) for intent in self.data["intents"] for pattern in intent["patterns"]]
        self.X = self.vectorizer.fit_transform(self.intent_patterns)

    def capture_face(self):
        _, frame = self.camera.get_frame()
        if frame is not None:
            image_path = self.camera.capture_image(frame)
            self.camera.release()
            return image_path
        return None  # No face detected

    def get_response(self, user_input, detected_lang):
        if detected_lang == "ur":
            user_input = self.translator.translate_to_english(user_input)  # ✅ Now using MachineTranslation

        processed_input = preprocess_text(user_input)
        intent, _, _, _ = get_intent(processed_input, self.vectorizer, self.X, self.data)

        response = "I'm sorry, I didn't understand. Could you rephrase?"  # Default fallback

        if intent:
            if intent["tag"] == "office_location":
                response = handle_department_query(user_input, self.data, self.intent_file)
            elif "responses" in intent and intent["responses"]:
                response = intent["responses"][0]

        # UNCOMMENT WHEN DEBUGGING
        if DEBUG_MODE:
            response = developer_override(user_input, response, self.data, self.intent_file, self.context_file)


        return response

        
    def log_interaction(self, user_input, response, face_path):
        """Logs interactions with face image instead of username."""
        log_entry = {
            "face_image": face_path if face_path else "No Face Detected",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": user_input,
            "answer": response
        }
        self.context["logs"].append(log_entry)
        save_json(self.context_file, self.context)
        reinforce_learning(user_input, response, self.data, self.intent_file)