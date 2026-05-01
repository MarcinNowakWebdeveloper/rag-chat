from backend.core.config import config
from backend.core.vector_store import get_vector_db


class RAGClassifier:
    def __init__(self, db):
        self.db = db

    def classify(self, question: str):
        results = self.db.similarity_search_with_score(question, k=3)

        if not results:
            return {"allowed": False, "confidence": 0.0}

        best_score = results[0][1]

        confidence = 1 - best_score

        if best_score < config.MIN_ALLOWED_TOPIC_SCORE:
            return True, confidence
        return False, confidence


db = get_vector_db()

classifier = RAGClassifier(db)
