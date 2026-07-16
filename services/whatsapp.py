"""
WhatsApp Cloud API Integration
Handles sending messages, managing templates, and verifying webhooks.
"""

import requests
import json
from config.settings import settings


class WhatsAppService:
    """
    WhatsApp Business API client for Meta Cloud API.
    Supports sending text/media messages, managing templates, and webhook verification.
    """

    def __init__(self):
        # Try Meta WhatsApp Cloud API first, fall back to Twilio
        self.token = settings.WHATSAPP_TOKEN or settings.TWILIO_AUTH_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.verify_token = settings.WHATSAPP_VERIFY_TOKEN
        self.twilio_account_sid = settings.TWILIO_ACCOUNT_SID
        self.twilio_auth_token = settings.TWILIO_AUTH_TOKEN
        self.twilio_whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.available = settings.has_whatsapp or settings.has_twilio
        self.using_twilio = settings.has_twilio and not settings.has_whatsapp

    def verify_webhook(self, verify_token, challenge):
        """
        Verify webhook subscription from Meta.
        Return challenge if verify_token matches.
        """
        if verify_token == self.verify_token:
            return challenge
        return None

    def send_message(self, recipient_number, message_text):
        """
        Send a simple text message.
        Args:
            recipient_number: WhatsApp phone number (with country code, e.g., +1234567890)
            message_text: Message text (max 4096 chars)
        Returns:
            dict with success status and message ID
        """
        if not self.available:
            return {"success": False, "error": "WhatsApp not configured"}

        url = f"{self.base_url}/{self.phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "text",
            "text": {"body": message_text},
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            data = response.json()

            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "message_id": data.get("messages", [{}])[0].get("id"),
                    "status": "sent",
                }
            else:
                error_msg = data.get("error", {}).get("message", "Unknown error")
                return {"success": False, "error": error_msg, "code": response.status_code}

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def send_template_message(self, recipient_number, template_name, language_code="en"):
        """
        Send a pre-approved WhatsApp template message.
        Args:
            recipient_number: WhatsApp phone number
            template_name: Name of approved template (e.g., 'order_confirmation')
            language_code: Language code (default 'en')
        Returns:
            dict with success status and message ID
        """
        if not self.available:
            return {"success": False, "error": "WhatsApp not configured"}

        url = f"{self.base_url}/{self.phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
            },
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            data = response.json()

            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "message_id": data.get("messages", [{}])[0].get("id"),
                    "status": "sent",
                }
            else:
                error_msg = data.get("error", {}).get("message", "Unknown error")
                return {"success": False, "error": error_msg}

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def send_media_message(self, recipient_number, media_url, media_type="image"):
        """
        Send a media message (image, video, document, audio).
        Args:
            recipient_number: WhatsApp phone number
            media_url: Direct URL to media file
            media_type: 'image', 'video', 'document', or 'audio'
        Returns:
            dict with success status and message ID
        """
        if not self.available:
            return {"success": False, "error": "WhatsApp not configured"}

        if media_type not in ["image", "video", "document", "audio"]:
            return {"success": False, "error": f"Invalid media type: {media_type}"}

        url = f"{self.base_url}/{self.phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": media_type,
            media_type: {"link": media_url},
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            data = response.json()

            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "message_id": data.get("messages", [{}])[0].get("id"),
                    "status": "sent",
                }
            else:
                error_msg = data.get("error", {}).get("message", "Unknown error")
                return {"success": False, "error": error_msg}

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def send_broadcast(self, recipient_numbers, message_text):
        """
        Send message to multiple recipients (broadcast).
        Args:
            recipient_numbers: List of WhatsApp phone numbers
            message_text: Message text
        Returns:
            dict with list of results for each recipient
        """
        results = []
        for number in recipient_numbers:
            result = self.send_message(number, message_text)
            results.append({"recipient": number, **result})
        return {"broadcast_id": f"broadcast_{len(results)}", "results": results}

    def parse_webhook_message(self, webhook_data):
        """
        Parse incoming WhatsApp message from webhook.
        Args:
            webhook_data: JSON payload from WhatsApp webhook
        Returns:
            dict with parsed message details or None
        """
        try:
            if webhook_data.get("object") != "whatsapp_business_account":
                return None

            entry = webhook_data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])

            if not messages:
                return None

            msg = messages[0]
            sender = msg.get("from")
            timestamp = msg.get("timestamp")

            # Extract message content
            msg_type = msg.get("type")  # text, image, video, document, audio, etc.
            text_body = None
            media_url = None

            if msg_type == "text":
                text_body = msg.get("text", {}).get("body")
            elif msg_type == "image":
                media_url = msg.get("image", {}).get("link")
            elif msg_type == "document":
                media_url = msg.get("document", {}).get("link")

            return {
                "from": sender,
                "message_id": msg.get("id"),
                "timestamp": timestamp,
                "type": msg_type,
                "text": text_body,
                "media_url": media_url,
            }

        except Exception as e:
            return None


# Singleton instance
whatsapp_service = WhatsAppService()
