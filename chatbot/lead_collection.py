"""
Lead Collection Module
"""

import re

from database.queries import save_lead


class LeadCollector:

    def valid_email(self, email):

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        return re.match(pattern, email)

    def valid_phone(self, phone):

        phone = phone.replace(" ", "")

        return phone.isdigit() and len(phone) >= 10

    def save(self, name, email, phone, interest, message, source="Website"):

        save_lead(
            name=name,
            email=email,
            phone=phone,
            interest=interest,
            message=message,
            source=source,
        )

        return "Lead Saved Successfully"
