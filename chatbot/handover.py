"""
Human Handover Module
"""

from database.queries import log_chat


class HumanHandover:

    def handover(self, session_id):

        response = (
            "👨‍💼 I understand you'd like to speak with a human representative.\n\n"
            "Your request has been forwarded to our support team.\n"
            "A SafeX representative will contact you shortly."
        )

        log_chat(
            session_id=session_id,
            role="assistant",
            message=response,
            language="en",
            intent="human_handover",
            matched_question=None,
            similarity=None,
            answered_by="handover",
            response_time=0
        )

        return response