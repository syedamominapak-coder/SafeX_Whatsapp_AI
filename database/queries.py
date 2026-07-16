from database.db import get_session

from database.models import Lead
from database.models import Conversation


# ------------------------
# LEADS
# ------------------------

def save_lead(
    name,
    email,
    phone,
    interest,
    message,
    source="Website"
):

    session = get_session()

    lead = Lead(

        name=name,

        email=email,

        phone=phone,

        interest=interest,

        message=message,

        source=source

    )

    session.add(lead)

    session.commit()

    session.close()


def get_all_leads():

    session = get_session()

    leads = session.query(Lead).all()

    session.close()

    return leads


# ------------------------
# CHAT HISTORY
# ------------------------

def log_chat(

    session_id,

    role,

    message,

    language,

    intent,

    matched_question,

    similarity,

    answered_by,

    response_time

):

    session = get_session()

    chat = Conversation(

        session_id=session_id,

        role=role,

        message=message,

        detected_language=language,

        intent=intent,

        matched_question=matched_question,

        similarity_score=similarity,

        answered_by=answered_by,

        response_time=response_time

    )

    session.add(chat)

    session.commit()

    session.close()


def get_all_conversations():

    session = get_session()

    rows = session.query(Conversation).all()

    session.close()

    return rows