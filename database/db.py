"""
SQLite Database Configuration
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

from config.constants import DB_PATH

os.makedirs("data", exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def init_db():

    Base.metadata.create_all(bind=engine)


def get_session():

    return SessionLocal()