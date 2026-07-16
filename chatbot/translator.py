"""
Translation Module
Uses deep-translator library to translate text between supported languages.
"""

from deep_translator import GoogleTranslator
from config.constants import SUPPORTED_LANGUAGES


class Translator:
    """
    Translates text between supported languages using Google Translate.
    """

    def __init__(self):
        self.supported_languages = SUPPORTED_LANGUAGES
        # Map our codes to Google Translate codes
        self.lang_map = {
            "en": "en",
            "ur": "ur",
            "ar": "ar",
            "fr": "fr",
            "es": "es",
        }

    def translate(self, text: str, target_lang: str = "en", source_lang: str = "auto") -> str:
        """
        Translate text to the target language.
        Args:
            text: Text to translate
            target_lang: Target language code (e.g., 'en', 'ur')
            source_lang: Source language code ('auto' for auto-detect)
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text

        target = self.lang_map.get(target_lang, "en")
        source = self.lang_map.get(source_lang, "auto") if source_lang != "auto" else "auto"

        try:
            translator = GoogleTranslator(source=source, target=target)
            return translator.translate(text)
        except Exception as e:
            # Fallback: return original text if translation fails
            return text

    def translate_to_english(self, text: str, source_lang: str = "auto") -> str:
        """
        Convenience method: translate any text to English.
        """
        return self.translate(text, target_lang="en", source_lang=source_lang)

    def translate_from_english(self, text: str, target_lang: str) -> str:
        """
        Convenience method: translate English text to target language.
        """
        return self.translate(text, target_lang=target_lang, source_lang="en")


# Singleton instance
translator = Translator()