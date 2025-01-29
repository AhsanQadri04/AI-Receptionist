from AI.Modules.JsonProcessing import save_json

def reinforce_learning(user_input, response, data, intent_file):
    failure_phrases = ["I'm sorry", "I don't understand", "Can you rephrase?"]

    if any(phrase in response for phrase in failure_phrases):
        # Ensure "unrecognized" category exists
        unrecognized_intent = next((intent for intent in data["intents"] if intent["tag"] == "unrecognized"), None)
        
        if not unrecognized_intent:
            data["intents"].append({
                "tag": "unrecognized",
                "patterns": [],
                "responses": ["I'm still learning. Can you rephrase?"]
            })
            unrecognized_intent = data["intents"][-1]

        unrecognized_intent["patterns"].append(user_input)
        save_json(intent_file, data)
