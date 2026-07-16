"""
Loads environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    APP_ENV = os.getenv("APP_ENV", "development")

    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # OpenRouter
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

    # HubSpot
    HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN", "")

    # WhatsApp - Meta Cloud API
    WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
    WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "")

    # WhatsApp - Twilio (fallback)
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "")

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

    # Webhook
    WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "5000"))

    @property
    def has_gemini(self):
        return self.GEMINI_API_KEY != ""

    @property
    def has_openrouter(self):
        return self.OPENROUTER_API_KEY != ""

    @property
    def has_hubspot(self):
        return self.HUBSPOT_ACCESS_TOKEN != ""

    @property
    def has_whatsapp(self):
        return (
            self.WHATSAPP_TOKEN != ""
            and self.WHATSAPP_PHONE_NUMBER_ID != ""
        )

    @property
    def has_twilio(self):
        return (
            self.TWILIO_ACCOUNT_SID != ""
            and self.TWILIO_AUTH_TOKEN != ""
        )


settings = Settings()