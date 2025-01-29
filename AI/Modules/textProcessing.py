import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    words = word_tokenize(text.lower())
    return " ".join([lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words])

def get_intent(user_input, vectorizer, X, data, threshold=0.4):
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X)[0]

    max_score = max(similarities, default=0)
    if max_score < threshold:
        return None, None, -1, max_score  

    best_match_index = similarities.argmax()
    matched_pattern = [preprocess_text(p) for intent in data["intents"] for p in intent["patterns"]][best_match_index]

    matched_intent = next(
        (intent for intent in data["intents"] if matched_pattern in [preprocess_text(p) for p in intent["patterns"]]), None
    )

    return matched_intent, matched_pattern, best_match_index, max_score
