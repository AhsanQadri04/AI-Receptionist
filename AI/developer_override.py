from AI.Modules.JsonProcessing import save_json, load_json
import logging

def developer_override(user_input, response, data, intent_file, context_file="AI/Data/context.json"):
    context = load_json(context_file, default_data={})
    context.setdefault("overrides", {})
    if user_input in context["overrides"]:
        logging.info(f"Using stored override for: {user_input}")
        return context["overrides"][user_input]
    dev_override = input(f"🤖 Chatbot: {response}\n Developer: Is this correct? (yes/no/override): ").strip().lower()
    if dev_override in ("no", "override"):
        correct_response = input("✅ Developer: Enter the correct response (or type 'skip' to cancel): ").strip()
        if correct_response.lower() == "skip" or not correct_response:
            logging.info("Override skipped. No changes were made.")
            return response
        context["overrides"][user_input] = correct_response
        save_json(context_file, context)
        correct_intent = input("🔹 Was this an incorrect voice recognition? (yes/no): ").strip().lower()
        if correct_intent == "no":
            for intent in data.get("intents", []):
                if user_input in intent.get("patterns", []):
                    if intent.get("responses"):
                        intent["responses"][0] = correct_response
                    else:
                        intent["responses"] = [correct_response]
                    break
            else:
                data.setdefault("intents", []).append({
                    "tag": "developer_override",
                    "patterns": [user_input],
                    "responses": [correct_response]
                })
            save_json(intent_file, data)
        print("✅ Correction saved! This mistake won’t be asked again.")
        return correct_response
    return response
