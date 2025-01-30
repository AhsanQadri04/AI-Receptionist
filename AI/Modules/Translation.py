from googletrans import Translator

class MachineTranslation:
    def __init__(self):
        self.translator = Translator()

    def translate_to_english(self, text):
        """Translates Urdu input to English before intent matching."""
        try:
            translated_text = self.translator.translate(text, src="ur", dest="en").text
            print(f"🔹 Translated Urdu to English: {translated_text}")  # Debugging
            return translated_text
        except Exception as e:
            print(f"❌ Translation Error: {e}")
            return text