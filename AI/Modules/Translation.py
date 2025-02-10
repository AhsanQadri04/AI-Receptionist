from googletrans import Translator
import logging

# Configure logging (adjust level and format as needed)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MachineTranslation:
    def __init__(self):
        self.translator = Translator()

    def translate_to_english(self, text):
        """
        Translates Urdu input to English before intent matching.

        Args:
            text (str): The input text in Urdu.

        Returns:
            str: The translated text in English. If translation fails or the input is empty,
                 the original text is returned.
        """
        if not text:
            logging.warning("Empty text provided for translation.")
            return text

        try:
            # Translate from Urdu ('ur') to English ('en')
            translated_text = self.translator.translate(text, src="ur", dest="en").text
            logging.info(f"🔹 Translated Urdu to English: {translated_text}")
            return translated_text
        except Exception as e:
            logging.error(f"❌ Translation Error: {e}")
            # Return the original text in case of any error
            return text
