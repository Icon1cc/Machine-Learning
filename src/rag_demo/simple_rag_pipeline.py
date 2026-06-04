"""A local, API-free RAG-style pipeline using TF-IDF retrieval."""

from __future__ import annotations

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class Document:
    doc_id: str
    text: str


DOCUMENTS = [
    Document("vacation", "Employees receive 20 vacation days each calendar year."),
    Document("expenses", "Expense reports must be submitted within 30 days of purchase."),
    Document("security", "All production systems require multi-factor authentication."),
]


class SimpleRAG:
    """Retrieve the most relevant local document and synthesize a grounded answer."""

    def __init__(self, documents: list[Document]) -> None:
        self.documents = documents
        self.vectorizer = TfidfVectorizer()
        self.matrix = self.vectorizer.fit_transform([doc.text for doc in documents])

    def retrieve(self, question: str, top_k: int = 2) -> list[tuple[Document, float]]:
        query_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)[:top_k]
        return [(self.documents[index], float(score)) for index, score in ranked]

    def answer(self, question: str) -> str:
        retrieved = self.retrieve(question, top_k=1)
        document, score = retrieved[0]
        if score <= 0:
            return "I do not have enough local context to answer that question."
        return f"Based on {document.doc_id}: {document.text}"


def demo() -> None:
    rag = SimpleRAG(DOCUMENTS)
    question = "How many vacation days do employees get?"
    print("Question:", question)
    print("Retrieved:", rag.retrieve(question))
    print("Answer:", rag.answer(question))


if __name__ == "__main__":
    demo()
