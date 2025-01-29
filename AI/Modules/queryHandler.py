def handle_department_query(user_input, data):

    office_intent = next((intent for intent in data["intents"] if intent["tag"] == "office_location"), None)

    if not office_intent or "hardcoded_locations" not in office_intent:
        return "Sorry, I don't have location data available."

    locations = office_intent["hardcoded_locations"]

    # Direct match lookup (case-insensitive)
    for department in locations:
        if department.lower() in user_input.lower():
            return locations[department]

    return "I'm not sure about that department. Can you specify which one you're looking for?"
