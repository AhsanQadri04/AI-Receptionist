from AI.Modules.JsonProcessing import save_json, load_json
import logging

def developer_override(user_input, response, data, intent_file, context_file="AI/Data/context.json"):
    """
    Allows the developer to override the chatbot's response if it's incorrect.

    This function loads a context file that stores previous developer overrides.
    If an override for the given user_input exists, it is used directly. Otherwise,
    the developer is prompted to confirm or provide an override. If an override is
    provided and voice recognition is determined to be correct (i.e. the error is in
    the response generation, not in the recognition), the corresponding intent's response
    is updated. The updated data is then saved to the context and intent files.

    Args:
        user_input (str): The user's input.
        response (str): The chatbot's original response.
        data (dict): The current intent data (with intents, patterns, and responses).
        intent_file (str): Path to the JSON file storing intent data.
        context_file (str): Path to the JSON file storing override context (default "AI/Data/context.json").

    Returns:
        str: The final response, either the original or the developer-corrected version.
    """
    # Load context and ensure the "overrides" key exists.
    context = load_json(context_file, default_data={})
    context.setdefault("overrides", {})

    # If an override already exists for this input, use it.
    if user_input in context["overrides"]:
        logging.info(f"Using stored override for: {user_input}")
        return context["overrides"][user_input]

    # Prompt the developer for feedback on the current response.
    dev_override = input(f"🤖 Chatbot: {response}\n Developer: Is this correct? (yes/no/override): ").strip().lower()

    if dev_override in ("no", "override"):
        correct_response = input("✅ Developer: Enter the correct response (or type 'skip' to cancel): ").strip()
        if correct_response.lower() == "skip" or not correct_response:
            logging.info("Override skipped. No changes were made.")
            return response

        # Store the override in the context.
        context["overrides"][user_input] = correct_response
        save_json(context_file, context)

        # Ask if the error was due to voice recognition.
        correct_intent = input("🔹 Was this an incorrect voice recognition? (yes/no): ").strip().lower()
        if correct_intent == "no":
            # Update the corresponding intent's response.
            for intent in data.get("intents", []):
                if user_input in intent.get("patterns", []):
                    if intent.get("responses"):
                        intent["responses"][0] = correct_response
                    else:
                        intent["responses"] = [correct_response]
                    break
            else:
                # No matching intent found; create a new override intent.
                data.setdefault("intents", []).append({
                    "tag": "developer_override",
                    "patterns": [user_input],
                    "responses": [correct_response]
                })

            save_json(intent_file, data)

        print("✅ Correction saved! This mistake won’t be asked again.")
        return correct_response

    return response
