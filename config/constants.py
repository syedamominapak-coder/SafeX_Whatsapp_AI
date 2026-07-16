"""
Application constants.
"""

APP_NAME = "SafeX AI Business Assistant"
APP_ICON = "🛡️"
APP_VERSION = "1.0.0"

COMPANY_NAME = "SafeX"

# ---------------- FAQ ---------------- #

FAQ_SIMILARITY_THRESHOLD = 0.60

FAQ_XLSX_PATH = "data/SafeX_200_FAQ_Dataset_new.xlsx"

FAQ_COL_QUESTION = "Question"
FAQ_COL_ALT_QUESTIONS = "Alternative Questions"
FAQ_COL_ANSWER = "Answer"
FAQ_COL_CATEGORY = "Category"
FAQ_COL_KEYWORDS = "Keywords"

FAQ_ALT_SEPARATOR = "|"

# ---------------- Database ---------------- #

DB_PATH = "data/safex_assistant.db"

# ---------------- Chat ---------------- #

DEFAULT_LANGUAGE = "en"

MAX_CHAT_HISTORY = 20

# ---------------- Greetings ---------------- #

GREETING_KEYWORDS = [
    "hi",
    "hello",
    "hey",
    "greetings",
    "good morning",
    "good afternoon",
    "good evening"
]

GOODBYE_KEYWORDS = [
    "bye",
    "goodbye",
    "see you",
    "thanks",
    "thank you"
]

# ---------------- Human ---------------- #

HANDOVER_KEYWORDS = [

    "human",
    "real human",
    "person",
    "someone",
    "agent",
    "support",

    "customer support",

    "technical support",

    "representative",

    "staff",

    "employee",

    "manager",

    "owner",

    "director",

    "ceo",

    "sales",

    "sales team",

    "talk to human",

    "connect me",

    "call me",

    "phone call"

]

# ---------------- Leads ---------------- #

LEAD_KEYWORDS = [

    "pricing",

    "price",

    "cost",

    "quote",

    "buy",

    "purchase",

    "order",

    "demo",

    "trial",

    "subscription",

    "interested",

    "contact me",

    "email me",

    "call me"

]

SUPPORTED_LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es"
}