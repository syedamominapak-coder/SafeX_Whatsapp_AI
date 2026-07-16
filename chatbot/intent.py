"""
Intent Detection Module
"""

import re

from config.constants import *


class IntentDetector:

    def __init__(self):

        self.greetings = GREETING_KEYWORDS

        self.goodbyes = GOODBYE_KEYWORDS

        self.handover = HANDOVER_KEYWORDS + [

            "person",
            "someone",
            "staff",
            "employee",
            "ceo",
            "owner",
            "director",
            "sales",
            "sales team",
            "technical support",
            "help desk"

        ]

        self.leads = LEAD_KEYWORDS

    def contains(self, message, keywords):

        words = set(re.findall(r"\b\w+\b", message))

        for keyword in keywords:

            keyword = keyword.lower()

            if " " in keyword:

                if keyword in message:
                    return True

            else:

                if keyword in words:
                    return True

        return False

    def detect(self, message):

        message = message.lower().strip()

        if self.contains(message, self.greetings):

            return "greeting"

        if self.contains(message, self.goodbyes):

            return "goodbye"

        if self.contains(message, self.handover):

            return "human_handover"

        if self.contains(message, self.leads):

            return "lead_capture"

        return "faq"