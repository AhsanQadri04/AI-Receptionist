from AI.Modules.learningModule import reinforce_learning
from AI.Modules.JsonProcessing import save_json

def handle_department_query(user_input, data, intent_file):
    """
    Ensures the chatbot only returns known department locations and properly learns new ones.
    If the department is not recognized, prompts the user to add a new location.
    """
    # Safely retrieve the 'office_location' intent from data
    office_intent = next(
        (intent for intent in data.get("intents", []) if intent.get("tag") == "office_location"),
        None
    )

    if not office_intent or "hardcoded_locations" not in office_intent:
        return "Sorry, I don't have location data available."

    locations = office_intent["hardcoded_locations"]

    # Normalize user input for comparison
    normalized_input = user_input.lower()

    # Check for a matching department in the known locations
    for department, location in locations.items():
        if department.lower() in normalized_input:
            return location  # Return the matched location immediately

    # If no matching department is found, ask if the chatbot should learn it
    confirm_learn = input(f"I don't recognize '{user_input}'. Would you like me to learn it? (yes/no): ").strip().lower()

    if confirm_learn == "yes":
        new_location = input(f"Great! Where is '{user_input}' located? ").strip()
        # Optionally, normalize the department key (e.g., using title() or lower())
        locations[user_input] = new_location
        save_json(intent_file, data)
        return f"Got it! '{user_input}' is now saved as: {new_location}."

    return "Alright! I won't learn that department."
