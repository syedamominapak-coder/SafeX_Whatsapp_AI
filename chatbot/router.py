"""
Routes user messages to the correct module.
"""

from chatbot.intent import IntentDetector
from chatbot.faq_engine import FAQEngine
from chatbot.handover import HumanHandover
from chatbot.openai_fallback import GeminiFallback

from config.constants import FAQ_SIMILARITY_THRESHOLD


class Router:

    def __init__(self):

        self.intent = IntentDetector()
        self.faq = FAQEngine()
        self.human = HumanHandover()
        self.ai = GeminiFallback()

    def reply(self, session_id, message):

        intent = self.intent.detect(message)

        # -------------------------------
        # Greeting
        # -------------------------------

        if intent == "greeting":

            return {
                "answer": (
                    "Welcome to SafeX.\n\n"
                    "How can I assist you today?"
                ),
                "confidence": 1.0,
                "category": "Greeting",
                "source": "Greeting",
            }

        # -------------------------------
        # Goodbye
        # -------------------------------

        if intent == "goodbye":

            return {
                "answer": (
                    "Thank you for contacting SafeX.\n"
                    "We appreciate your time and wish you a great day."
                ),
                "confidence": 1.0,
                "category": "Goodbye",
                "source": "Goodbye",
            }

        # -------------------------------
        # Human Handover
        # -------------------------------

        if intent == "human_handover":

            return {
                "answer": self.human.handover(session_id),
                "confidence": 1.0,
                "category": "Human Support",
                "source": "Human",
            }

        # -------------------------------
        # FAQ Search
        # -------------------------------

        faq = self.faq.ask(message)

        if faq["matched"]:

            return {
                "answer": faq["answer"],
                "confidence": faq["confidence"],
                "category": faq["category"],
                "source": "FAQ",
            }

        # -------------------------------
        # Gemini Fallback
        # -------------------------------

        ai_answer = self.ai.generate(message)

        return {
            "answer": ai_answer,
            "confidence": faq["confidence"],
            "category": "AI",
            "source": "Gemini",
        }