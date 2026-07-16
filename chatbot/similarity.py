"""
TF-IDF Similarity Engine

Uses:
- TF-IDF
- Cosine Similarity
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityEngine:

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            stop_words="english"
        )

        self.matrix = None

    def fit(self, corpus):

        self.matrix = self.vectorizer.fit_transform(corpus)

    def search(self, query):

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.matrix
        )

        return scores.flatten()