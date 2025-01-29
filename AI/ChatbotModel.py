import json
import os
import random
import logging
import difflib
import time
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from langdetect import detect

# Setup logging
logging.basicConfig(filename="AI/Data/chatbot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class Chatbot:
    def __init__(self, intent_file="AI/Data/intent.json", context_file="AI/Data/context.json"):
        self.intent_file = intent_file
        self.context_file = context_file
        self.data = self.load_json(intent_file)
        self.context = self.load_json(context_file, default_data={"logs": []})
        
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        self.last_input_time = time.time()
        self.user_name = None  # Store the user's name

        # Train TF-IDF model
        self.vectorizer = TfidfVectorizer()
        self.intent_patterns = [self.preprocess_text(pattern) for intent in self.data.get("intents", []) for pattern in intent["patterns"]]
        self.X = self.vectorizer.fit_transform(self.intent_patterns)

    def load_json(self, filename, default_data=None):
        if not os.path.exists(filename):
            print(f"Warning: {filename} not found. Creating a new one.")
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(default_data, file, indent=4)
        try:
            with open(filename, encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Warning: {filename} is corrupted. Resetting to default.")
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(default_data, file, indent=4)
            return default_data

    def save_json(self, filename, data):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def preprocess_text(self, text):
        words = word_tokenize(text.lower())
        return " ".join([self.lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in self.stop_words])

    def get_intent(self, user_input, threshold=0.4):
        user_vec = self.vectorizer.transform([user_input])
        similarities = cosine_similarity(user_vec, self.X)[0]
        
        max_score = max(similarities, default=0)
        if max_score < threshold:
            return None, None, -1, max_score  

        best_match_index = similarities.argmax()
        matched_pattern = self.intent_patterns[best_match_index]

        matched_intent = next(
            (intent for intent in self.data["intents"] if matched_pattern in [self.preprocess_text(p) for p in intent["patterns"]]), None
        )

        return matched_intent, matched_pattern, best_match_index, max_score

    def ask_for_name(self):
        if self.user_name is None:
            self.user_name = input("Hello! What is your name? (Press Enter to skip): ").strip()
            if not self.user_name:
                self.user_name = "Anonymous"
            print(f"Nice to meet you, {self.user_name}! How can I assist you today?")
        return self.user_name

    def log_interaction(self, user_input, response):
        log_entry = {
            "username": self.user_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": user_input,
            "answer": response
        }
        self.context["logs"].append(log_entry)
        self.save_json(self.context_file, self.context)

    def handle_department_query(self, user_input):
        office_intent = next((intent for intent in self.data["intents"] if intent["tag"] == "office_location"), None)
        
        if not office_intent or "hardcoded_locations" not in office_intent:
            return "Sorry, I don't have location data available."
        
        locations = office_intent["hardcoded_locations"]
        best_match = max(locations.keys(), key=lambda loc: fuzz.partial_ratio(user_input.lower(), loc.lower()))
        
        if fuzz.partial_ratio(user_input.lower(), best_match.lower()) > 80:
            return f"The {best_match} department is located at {locations[best_match]}"
        
        return "Sorry, I couldn't find that department."

    def get_response(self, user_input):
        self.ask_for_name()
        
        user_input = user_input.strip().lower()
        if not user_input:
            return "I'm sorry, I didn't catch that. Could you say it again?"

        processed_input = self.preprocess_text(user_input)
        intent, pattern, pattern_index, similarity_score = self.get_intent(processed_input)

        if intent:
            if intent["tag"] == "office_location":
                response = self.handle_department_query(user_input)
            else:
                response = random.choice(intent["responses"])

            self.log_interaction(user_input, response)

            if intent["tag"] == "goodbye":
                print("Ending session as 'goodbye' was detected.")
                return response

            self.last_input_time = time.time()
            return response

        return "I'm sorry, I didn't understand. Could you rephrase?"

    def auto_end_session(self):
        while True:
            if time.time() - self.last_input_time > 3:
                print("No response received. Ending session.")
                break
            time.sleep(1)
