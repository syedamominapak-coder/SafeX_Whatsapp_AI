"""
Text preprocessing utilities.
"""

import re
import string
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download only once
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


def preprocess_text(text: str) -> str:
    """
    Clean and normalize text before TF-IDF.
    """

    if text is None:
        return ""

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = re.sub(r"\s+", " ", text).strip()

    words = []

    for word in text.split():

        if word not in STOP_WORDS:

            words.append(
                LEMMATIZER.lemmatize(word)
            )

    return " ".join(words)