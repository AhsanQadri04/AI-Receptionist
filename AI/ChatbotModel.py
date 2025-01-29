import random
import time
import logging
from datetime import datetime
from AI.Modules.JsonProcessing import load_json, save_json
from AI.Modules.textProcessing import preprocess_text, get_intent
from AI.Modules.queryHandler import handle_department_query
from AI.Modules.learningModule import reinforce_learning
from sklearn.feature_extraction.text import TfidfVectorizer

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

        # Train TF-IDF model
        self.vectorizer = TfidfVectorizer()
        self.intent_patterns = [preprocess_text(pattern) for intent in self.data["intents"] for pattern in intent["patterns"]]
        self.X = self.vectorizer.fit_transform(self.intent_patterns)

    def ask_for_name(self):
        if self.user_name is None:
            self.user_name = input("Hello! What is your name? (Press Enter to skip): ").strip()
            if not self.user_name:
                self.user_name = "Anonymous"
            print(f"Nice to meet you, {self.user_name}! How can I assist you today?")

    def get_response(self, user_input):
        self.ask_for_name()
        user_input = preprocess_text(user_input)
        intent, _, _, _ = get_intent(user_input, self.vectorizer, self.X, self.data)

        if intent:
            response = handle_department_query(user_input, self.data) if intent["tag"] == "office_location" else random.choice(intent["responses"])
        else:
            response = "I'm sorry, I didn't understand. Could you rephrase?"

        self.log_interaction(user_input, response)
        return response

    def log_interaction(self, user_input, response):
        self.context["logs"].append({
            "username": self.user_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": user_input,
            "answer": response
        })
        save_json(self.context_file, self.context)
        reinforce_learning(user_input, response, self.data, self.intent_file)
