from AI.Modules.JsonProcessing import save_json

def reinforce_learning(user_input, response, data, intent_file):
    """Updates the chatbot training data when it fails to recognize user input."""
    
    failure_phrases = ["i'm sorry", "i don't understand", "can you rephrase?"]
    
    if any(phrase in response.lower() for phrase in failure_phrases):
        
        # Ensure "intents" key exists
        if "intents" not in data:
            data["intents"] = []
        
        # Find or create the "unrecognized" intent category
        unrecognized_intent = next((intent for intent in data["intents"] if intent["tag"] == "unrecognized"), None)
        
        if not unrecognized_intent:
            unrecognized_intent = {
                "tag": "unrecognized",
                "patterns": [],
                "responses": ["I'm still learning. Can you rephrase?"]
            }
            data["intents"].append(unrecognized_intent)

        # Ensure unique entries (avoid duplicate user inputs)
        if user_input not in unrecognized_intent["patterns"]:
            unrecognized_intent["patterns"].append(user_input)
            save_json(intent_file, data)  # Save only when an update is made
