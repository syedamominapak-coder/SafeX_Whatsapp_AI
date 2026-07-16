"""
Language Detection Service
Detects language from user messages and provides language utilities.
"""

import re
from config.constants import SUPPORTED_LANGUAGES


# Simple keyword-based language detection for common languages
LANGUAGE_PATTERNS = {
    "en": {
        "name": "English",
        "patterns": [
            r"\b(the|is|are|how|what|where|when|who|this|that|please|thanks|help|hello|hi)\b",
        ],
    },
    "ur": {
        "name": "Urdu",
        "patterns": [
            r"\b(کیا|ہے|ہیں|اور|سے|کا|کی|کے|میں|پر|آپ|یہ|وہ|نہیں|ہو|گا|گی)\b",
        ],
    },
    "ar": {
        "name": "Arabic",
        "patterns": [
            r"\b(ما|هو|هي|هل|كيف|أين|متى|من|هذا|هذه|مرحبا|شكرا|مساعدة)\b",
        ],
    },
    "fr": {
        "name": "French",
        "patterns": [
            r"\b(le|la|les|est|sont|comment|quoi|où|quand|qui|ce|cet|cette|bonjour|merci|aide)\b",
        ],
    },
    "es": {
        "name": "Spanish",
        "patterns": [
            r"\b(el|la|los|las|es|son|cómo|qué|dónde|cuándo|quién|este|esta|hola|gracias|ayuda)\b",
        ],
    },
}


class LanguageService:
    """
    Detects language from text and provides translation-ready utilities.
    """

    def __init__(self):
        self.supported_languages = SUPPORTED_LANGUAGES

    def detect(self, text: str) -> str:
        """
        Detect language code from text using keyword patterns.
        Returns ISO language code (e.g., 'en', 'ur').
        """
        if not text:
            return "en"

        text_lower = text.lower().strip()
        scores = {}

        for lang_code, lang_info in LANGUAGE_PATTERNS.items():
            score = 0
            for pattern in lang_info["patterns"]:
                matches = re.findall(pattern, text_lower)
                score += len(matches)
            if score > 0:
                scores[lang_code] = score

        if not scores:
            return "en"

        return max(scores, key=scores.get)

    def get_language_name(self, lang_code: str) -> str:
        """
        Get the human-readable language name from a language code.
        """
        reverse_map = {v: k for k, v in self.supported_languages.items()}
        return reverse_map.get(lang_code, "English")

    def is_supported(self, lang_code: str) -> bool:
        """
        Check if a language code is supported.
        """
        return lang_code in self.supported_languages.values()


# Singleton instance
language_service = LanguageService()