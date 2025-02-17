from AI.Modules.JsonProcessing import save_json

def reinforce_learning(user_input, response, data, intent_file):
    failure_phrases = ["i'm sorry", "i don't understand", "can you rephrase?"]
    if any(phrase in response.lower() for phrase in failure_phrases):
        if "intents" not in data:
            data["intents"] = []
        unrecognized_intent = next((intent for intent in data["intents"] if intent["tag"] == "unrecognized"), None)
        if not unrecognized_intent:
            unrecognized_intent = {
                "tag": "unrecognized",
                "patterns": [],
                "responses": ["I'm still learning. Can you rephrase?"]
            }
            data["intents"].append(unrecognized_intent)
        if user_input not in unrecognized_intent["patterns"]:
            unrecognized_intent["patterns"].append(user_input)
            save_json(intent_file, data)
