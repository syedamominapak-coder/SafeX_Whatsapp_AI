from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Text
from sqlalchemy import DateTime

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Lead(Base):

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)

    name = Column(String(100))

    email = Column(String(100))

    phone = Column(String(30))

    interest = Column(String(150))

    message = Column(Text)

    status = Column(
        String(30),
        default="New"
    )

    crm_synced = Column(
        String(10),
        default="No"
    )

    source = Column(
        String(30),
        default="Website"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)

    session_id = Column(String(100))

    role = Column(String(20))

    message = Column(Text)

    detected_language = Column(
        String(10),
        default="en"
    )

    intent = Column(String(50))

    matched_question = Column(Text)

    similarity_score = Column(Float)

    answered_by = Column(String(20))

    response_time = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )