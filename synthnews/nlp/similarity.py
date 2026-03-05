from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import numpy as np


def collect_text(path: str) -> str:
    """Collects all text for a particular topic"""

    texts = []

    p = Path(path)

    for txtfile in p.iterdir():
        if txtfile.is_file() and txtfile.suffix == ".txt":
            with open(txtfile, "r") as f:
                texts.append(f.read())

    return texts


def create_corpus(texts: List[str]) -> Tuple[TfidfVectorizer, np.ndarray]:
    """Build TF-IDF corpus from texts. Returns (vectorizer, document-term matrix)."""
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix


def compute_similarity(
    corpus: Tuple[TfidfVectorizer, np.ndarray], text: str
) -> float:
    """
    Compute a score in [0, 1] for how similar text is to the corpus.
    Uses average cosine similarity across all documents in the corpus.
    """
    vectorizer, corpus_matrix = corpus
    text_vector = vectorizer.transform([text])
    similarities = cosine_similarity(text_vector, corpus_matrix)
    return float(np.mean(similarities))
