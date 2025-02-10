from fuzzywuzzy import process
from spellchecker import SpellChecker
import json

class TextProcessor:
    def __init__(self, intent_file_path):
        # Load intents from the provided JSON file
        self.intents = self.load_intents(intent_file_path)
        self.spell = SpellChecker()

    def load_intents(self, intent_file_path):
        with open(intent_file_path, 'r') as file:
            return json.load(file)

    def fuzzy_match(self, user_input):
        best_match = None
        best_score = 0

        # Iterate through all intents and their patterns
        for intent in self.intents:
            for pattern in intent['patterns']:
                score = process.extractOne(user_input, [pattern])[1]
                if score > best_score:
                    best_score = score
                    best_match = intent

        return best_match if best_score >= 80 else None  # You can adjust the threshold

    def correct_spelling(self, text):
        # Correct the spelling of the input text
        corrected_text = ' '.join([self.spell.correction(word) for word in text.split()])
        return corrected_text
