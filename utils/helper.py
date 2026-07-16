"""
Helper Utilities
General-purpose helper functions for the SafeX AI Assistant.
"""

import re
import uuid
from datetime import datetime


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


def format_timestamp(dt: datetime = None, fmt: str = "%I:%M %p") -> str:
    """Format a datetime object to a readable time string."""
    if dt is None:
        dt = datetime.utcnow()
    return dt.strftime(fmt)


def sanitize_text(text: str) -> str:
    """Remove excessive whitespace and normalize text."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to a maximum length, adding ellipsis if needed."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."


def mask_email(email: str) -> str:
    """Mask an email address for privacy: j***@example.com"""
    if not email or "@" not in email:
        return email
    name, domain = email.split("@", 1)
    if len(name) <= 1:
        return f"{name}***@{domain}"
    return f"{name[0]}***@{domain}"


def mask_phone(phone: str) -> str:
    """Mask a phone number: +92***1234"""
    if not phone:
        return phone
    if len(phone) <= 6:
        return phone[:2] + "***" + phone[-2:]
    return phone[:3] + "***" + phone[-4:]