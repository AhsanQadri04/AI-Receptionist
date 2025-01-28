import nltk
import json
import random
import os
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz

nltk.download('punkt')
nltk.download('stopwords')

class Chatbot:
    def __init__(self, intent_file='AI/intent.json', context_file='AI/context.json'):
        self.intent_file = intent_file
        self.context_file = context_file
        self.data = self.load_intents()
        self.context = self.load_context()
        self.stop_words = set(stopwords.words('english'))
        self.time_greetings = {"morning": (5, 12), "afternoon": (12, 17), "evening": (17, 21)}

    def load_intents(self):
        try:
            with open(self.intent_file) as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"intents": []}

    def load_context(self):
        if os.path.exists(self.context_file):
            with open(self.context_file, 'r') as file:
                return json.load(file)
        return {"user_name": "", "last_intent": "", "previous_query": ""}

    def save_context(self):
        with open(self.context_file, 'w') as file:
            json.dump(self.context, file)

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        return [word for word in tokens if word.isalnum() and word not in self.stop_words]

    def get_time_based_greeting(self):
        current_hour = datetime.now().hour
        for part, (start, end) in self.time_greetings.items():
            if start <= current_hour < end:
                return part
        return "day"

    def get_intent(self, user_input, threshold=70):
        max_score = 0
        matched_intent = None
        for intent in self.data['intents']:
            for pattern in intent['patterns']:
                score = fuzz.partial_ratio(user_input.lower(), pattern.lower())
                if score > max_score:
                    max_score = score
                    matched_intent = intent
        return matched_intent if max_score > threshold else None

    def handle_meeting_schedule(self, query):
        for meeting, details in self.meetings.items():
            if meeting in query.lower():
                return f"The {meeting} is scheduled at {details}."
        return "Please check the meeting name or contact the organizer for confirmation."

    def get_response(self, user_input):
        user_input = user_input.strip().lower()
        if not user_input:
            return "I'm sorry, I didn't catch that. Could you say it again?"
        intent = self.get_intent(user_input)
        if intent:
            if intent['tag'] == 'meeting_schedule':
                return self.handle_meeting_schedule(user_input)
            if 'context' in intent:
                self.context['last_intent'] = intent['tag']
                self.context['previous_query'] = user_input
            if intent['tag'] == 'greeting':
                time_part = self.get_time_based_greeting()
                return random.choice(intent['responses']).replace("[morning/afternoon/evening]", time_part)
            return random.choice(intent['responses'])
        return "I'm sorry, I didn't understand. Could you rephrase?"
