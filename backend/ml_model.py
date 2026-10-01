"""
ml_model.py
-----------
Optional: train a TF-IDF + cosine-similarity job-role classifier.
This module can be run standalone to produce a serialised model,
or imported by nlp_analyzer for richer scoring.

Usage:
    python ml_model.py          # trains and saves the model
"""

import json
import pickle
import math
from collections import Counter
from skills_data import JOB_ROLES, SKILLS_DB


# ── tiny synthetic training corpus ───────────────────────────────────────────
# Each role gets a short representative document built from its skill list.

def _build_corpus() -> tuple[list[str], list[str]]:
    docs, labels = [], []
    for role, spec in JOB_ROLES.items():
        # repeat required skills 3×, preferred 2× to simulate real frequency
        words = spec["required"] * 3 + spec["preferred"] * 2
        docs.append(" ".join(words))
        labels.append(role)
    return docs, labels


# ── TF-IDF vectoriser (hand-rolled, no sklearn needed) ───────────────────────

class TFIDFVectorizer:
    """Minimal TF-IDF vectoriser for skill-bag documents."""

    def __init__(self):
        self.vocab: list[str] = []
        self.idf:   dict[str, float] = {}

    # --- fit ---------------------------------------------------------------
    def fit(self, documents: list[str]) -> "TFIDFVectorizer":
        N = len(documents)
        df: Counter = Counter()

        tokenized = [doc.split() for doc in documents]
        for tokens in tokenized:
            for term in set(tokens):
                df[term] += 1

        self.vocab = sorted(df.keys())
        self.idf   = {t: math.log((N + 1) / (df[t] + 1)) + 1 for t in self.vocab}
        return self

    # --- transform ---------------------------------------------------------
    def transform(self, documents: list[str]) -> list[dict[str, float]]:
        vectors = []
        for doc in documents:
            tokens = doc.split()
            total  = max(len(tokens), 1)
            tf: Counter = Counter(tokens)
            vec = {
                t: (tf[t] / total) * self.idf.get(t, 0)
                for t in self.vocab
                if tf[t]
            }
            vectors.append(vec)
        return vectors

    def fit_transform(self, documents: list[str]) -> list[dict[str, float]]:
        self.fit(documents)
        return self.transform(documents)


# ── cosine-similarity classifier ─────────────────────────────────────────────

class CosineSimilarityClassifier:
    """
    Stores per-class centroid vectors.
    Predicts by finding the class whose centroid is closest to the query.
    """

    def __init__(self):
        self.centroids: dict[str, dict[str, float]] = {}

    @staticmethod
    def _magnitude(v: dict) -> float:
        return math.sqrt(sum(x * x for x in v.values()))

    @staticmethod
    def _cosine(a: dict, b: dict) -> float:
        keys = set(a) & set(b)
        if not keys:
            return 0.0
        dot   = sum(a[k] * b[k] for k in keys)
        mag_a = CosineSimilarityClassifier._magnitude(a)
        mag_b = CosineSimilarityClassifier._magnitude(b)
        return dot / (mag_a * mag_b) if (mag_a * mag_b) else 0.0

    def fit(self, vectors: list[dict], labels: list[str]) -> "CosineSimilarityClassifier":
        from collections import defaultdict
        buckets: dict[str, list] = defaultdict(list)
        for vec, lbl in zip(vectors, labels):
            buckets[lbl].append(vec)

        for lbl, vecs in buckets.items():
            # centroid = average of vectors
            all_keys: set = set().union(*vecs)
            centroid = {
                k: sum(v.get(k, 0) for v in vecs) / len(vecs)
                for k in all_keys
            }
            self.centroids[lbl] = centroid
        return self

    def predict_proba(self, vector: dict) -> list[tuple[str, float]]:
        scores = [
            (lbl, self._cosine(vector, centroid))
            for lbl, centroid in self.centroids.items()
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def predict(self, vector: dict) -> str:
        return self.predict_proba(vector)[0][0]


# ── full pipeline ─────────────────────────────────────────────────────────────

class ResumeRoleClassifier:
    """Combines TFIDFVectorizer + CosineSimilarityClassifier."""

    def __init__(self):
        self.vectorizer  = TFIDFVectorizer()
        self.classifier  = CosineSimilarityClassifier()
        self._is_trained = False

    def train(self) -> "ResumeRoleClassifier":
        docs, labels = _build_corpus()
        vectors = self.vectorizer.fit_transform(docs)
        self.classifier.fit(vectors, labels)
        self._is_trained = True
        print(f"[ML] Trained on {len(docs)} role documents.")
        return self

    def predict(self, skills: list[str]) -> list[tuple[str, float]]:
        """Given a list of skills, return ranked (role, confidence%) pairs."""
        if not self._is_trained:
            self.train()
        doc    = " ".join(skills)
        vector = self.vectorizer.transform([doc])[0]
        proba  = self.classifier.predict_proba(vector)
        # normalise scores to 0-100
        top = proba[0][1] if proba else 1
        return [(role, round(score / max(top, 1e-9) * 100, 1)) for role, score in proba]

    def save(self, path: str = "resume_classifier.pkl") -> None:
        with open(path, "wb") as f:
            pickle.dump(self, f)
        print(f"[ML] Model saved to {path}")

    @classmethod
    def load(cls, path: str = "resume_classifier.pkl") -> "ResumeRoleClassifier":
        with open(path, "rb") as f:
            obj = pickle.load(f)
        print(f"[ML] Model loaded from {path}")
        return obj


# ── standalone training ───────────────────────────────────────────────────────

if __name__ == "__main__":
    clf = ResumeRoleClassifier()
    clf.train()
    clf.save()

    # quick smoke-test
    test_skills = ["python", "machine learning", "tensorflow", "pandas", "sql"]
    results = clf.predict(test_skills)
    print("\n[ML] Smoke-test predictions:")
    for role, conf in results[:3]:
        print(f"  {role:35s} {conf:.1f}%")
