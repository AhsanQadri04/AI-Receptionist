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
    """
    Lowercases, tokenizes, filters non-alphanumeric tokens and stopwords, and lemmatizes the words.
    """
    words = word_tokenize(text.lower())
    return " ".join([lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words])

def get_intent(user_input, vectorizer, X, data, threshold=0.4):
    """
    Identifies the best matching intent for a given user input.
    
    Args:
        user_input (str): The input string from the user.
        vectorizer (TfidfVectorizer): The TF-IDF vectorizer pre-fitted on your corpus.
        X (sparse matrix): TF-IDF matrix corresponding to the flattened list of patterns.
        data (dict): A dictionary containing intents. Each intent should have a "tag" and a list of "patterns".
        threshold (float): Minimum cosine similarity to consider a match valid.
        
    Returns:
        tuple: (matched_intent, matched_pattern, best_match_index, max_score)
               If no intent meets the threshold, returns (None, None, -1, max_score).
    """
    # If your vectorizer was trained on preprocessed text, consider uncommenting the next line:
    # user_input = preprocess_text(user_input)
    
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X)[0]

    max_score = max(similarities, default=0)
    if max_score < threshold:
        return None, None, -1, max_score

    best_match_index = similarities.argmax()
    
    # Flatten and preprocess all patterns from the intents
    flattened_patterns = [
        preprocess_text(p) 
        for intent in data.get("intents", []) 
        for p in intent.get("patterns", [])
    ]
    
    # Ensure the index is within bounds
    if best_match_index >= len(flattened_patterns):
        return None, None, best_match_index, max_score

    matched_pattern = flattened_patterns[best_match_index]

    # Retrieve the intent that contains this matched pattern.
    matched_intent = next(
        (
            intent for intent in data.get("intents", [])
            if matched_pattern in [preprocess_text(p) for p in intent.get("patterns", [])]
        ),
        None
    )

    return matched_intent, matched_pattern, best_match_index, max_score
