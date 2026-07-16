"""
SafeX FAQ Engine

Hybrid Retrieval:
- TF-IDF + Cosine Similarity
- RapidFuzz
"""

import pandas as pd
from rapidfuzz import fuzz

from chatbot.preprocessing import preprocess_text
from chatbot.similarity import SimilarityEngine

from config.constants import *


class FAQEngine:

    def __init__(self):

        self.questions = []
        self.answers = []
        self.categories = []

        self.processed_questions = []

        self.engine = SimilarityEngine()

        self.load_dataset()

    def load_dataset(self):

        df = pd.read_excel(FAQ_XLSX_PATH)

        expanded_questions = []
        expanded_answers = []
        expanded_categories = []

        for _, row in df.iterrows():

            question = str(row[FAQ_COL_QUESTION]).strip()

            answer = str(row[FAQ_COL_ANSWER]).strip()

            category = str(row[FAQ_COL_CATEGORY]).strip()

            expanded_questions.append(question)
            expanded_answers.append(answer)
            expanded_categories.append(category)

            alt = row.get(FAQ_COL_ALT_QUESTIONS, "")

            if pd.notna(alt):

                for q in str(alt).split(FAQ_ALT_SEPARATOR):

                    q = q.strip()

                    if q:

                        expanded_questions.append(q)
                        expanded_answers.append(answer)
                        expanded_categories.append(category)

        processed = [
            preprocess_text(q)
            for q in expanded_questions
        ]

        self.questions = expanded_questions
        self.answers = expanded_answers
        self.categories = expanded_categories
        self.processed_questions = processed

        self.engine.fit(processed)

    def ask(self, user_question):

        processed = preprocess_text(user_question)

        cosine_scores = self.engine.search(processed)

        best_index = cosine_scores.argmax()

        cosine_score = float(cosine_scores[best_index])

        fuzzy_score = fuzz.token_sort_ratio(
            processed,
            self.processed_questions[best_index]
        ) / 100

        confidence = (
            0.7 * cosine_score +
            0.3 * fuzzy_score
        )

        return {

            "question": self.questions[best_index],

            "answer": self.answers[best_index],

            "category": self.categories[best_index],

            "confidence": round(confidence, 3),

            "matched": confidence >= FAQ_SIMILARITY_THRESHOLD

        }