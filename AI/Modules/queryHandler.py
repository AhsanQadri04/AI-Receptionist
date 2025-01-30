from AI.Modules.learningModule import reinforce_learning
from AI.Modules.JsonProcessing import save_json

def handle_department_query(user_input, data, intent_file):
    """Ensures chatbot only returns known department locations and properly learns new ones."""
    office_intent = next((intent for intent in data["intents"] if intent["tag"] == "office_location"), None)

    if not office_intent or "hardcoded_locations" not in office_intent:
        return "Sorry, I don't have location data available."

    locations = office_intent["hardcoded_locations"]

    for department, location in locations.items():
        if department.lower() in user_input.lower():
            return location  # ✅ Always returns the correct department

    confirm_learn = input(f"I don't recognize '{user_input}'. Would you like me to learn it? (yes/no): ").strip().lower()

    if confirm_learn == "yes":
        new_location = input(f"Great! Where is '{user_input}' located? ").strip()

        locations[user_input] = new_location
        save_json(intent_file, data)

        return f"Got it! '{user_input}' is now saved as: {new_location}."

    return "Alright! I won't learn that department."
