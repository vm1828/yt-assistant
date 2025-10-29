import os
from abc import ABC, abstractmethod
from typing import List

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sentence_transformers import SentenceTransformer


class EmbeddingAdapter(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Return embeddings for a list of texts"""
        pass


class LocalEmbeddingAdapter(EmbeddingAdapter):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()


class GoogleEmbeddingAdapter(EmbeddingAdapter):
    def __init__(self, model: str = "models/embedding-001"):
        self.model = GoogleGenerativeAIEmbeddings(
            model=model,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.embed_documents(texts)


# lazy init of embedding adapter
_emb_adapter = None


def get_emb_adapter(local: bool = False) -> EmbeddingAdapter:
    """Return a singleton embedding adapter using adapter pattern"""
    global _emb_adapter
    if (_emb_adapter is None) and local:
        return LocalEmbeddingAdapter()
    return GoogleEmbeddingAdapter()
