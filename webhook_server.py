"""
WhatsApp Webhook Handler
Receives incoming WhatsApp messages, routes them through the AI system, and sends replies.
Run separately from Streamlit: python webhook_server.py
"""

from flask import Flask, request, jsonify
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
from chatbot.router import Router
from services.whatsapp import whatsapp_service
from database.queries import log_chat

app = Flask(__name__)
router = Router()

# Store mapping of WhatsApp session IDs
SESSIONS = {}


@app.route("/webhook/whatsapp", methods=["GET"])
def webhook_verify():
    """
    Verify WhatsApp webhook subscription.
    GET /webhook/whatsapp?hub.mode=subscribe&hub.challenge=XXX&hub.verify_token=YYY
    """
    verify_token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    result = whatsapp_service.verify_webhook(verify_token, challenge)
    if result:
        return result, 200
    return "Invalid verify token", 403


@app.route("/webhook/whatsapp", methods=["POST"])
def webhook_receive():
    """
    Receive incoming WhatsApp messages and send AI responses.
    POST /webhook/whatsapp with JSON payload from WhatsApp
    """
    try:
        data = request.get_json()

        # Parse incoming message
        msg_info = whatsapp_service.parse_webhook_message(data)
        if not msg_info:
            return jsonify({"status": "no_message"}), 200

        sender = msg_info["from"]
        message_text = msg_info["text"]

        # Create or get session ID for this sender
        if sender not in SESSIONS:
            SESSIONS[sender] = f"whatsapp_{sender}"
        session_id = SESSIONS[sender]

        # Log incoming message
        if message_text:
            log_chat(
                session_id=session_id,
                role="user",
                message=message_text,
                language="en",
                intent="whatsapp_incoming",
                matched_question=None,
                similarity=None,
                answered_by="WhatsApp",
                response_time=0,
            )

            # Get AI response
            try:
                response = router.reply(session_id, message_text)
                bot_reply = response["answer"]

                # Log response
                log_chat(
                    session_id=session_id,
                    role="assistant",
                    message=bot_reply,
                    language="en",
                    intent="whatsapp_response",
                    matched_question=response.get("matched_question"),
                    similarity=response.get("confidence"),
                    answered_by=response.get("source", "AI"),
                    response_time=0,
                )

                # Send reply via WhatsApp
                send_result = whatsapp_service.send_message(sender, bot_reply)
                if not send_result["success"]:
                    print(f"Error sending message: {send_result['error']}")

            except Exception as e:
                error_msg = f"⚠️ Sorry, I encountered an error processing your message. Please try again."
                log_chat(
                    session_id=session_id,
                    role="assistant",
                    message=error_msg,
                    language="en",
                    intent="error",
                    matched_question=None,
                    similarity=0,
                    answered_by="Error Handler",
                    response_time=0,
                )
                whatsapp_service.send_message(sender, error_msg)
                print(f"Router error: {str(e)}")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "whatsapp-webhook"}), 200


if __name__ == "__main__":
    port = int(os.getenv("WEBHOOK_PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    print(f"Starting WhatsApp webhook server on port {port}...")
    print(f"Webhook URL: http://localhost:{port}/webhook/whatsapp")
    app.run(host="0.0.0.0", port=port, debug=debug)
