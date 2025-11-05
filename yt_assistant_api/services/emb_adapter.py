# TODO Package and share between api and emb service 

import asyncio
import os
from abc import ABC, abstractmethod
from typing import List

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sentence_transformers import SentenceTransformer


class EmbeddingAdapter(ABC):
    @abstractmethod
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Return embeddings for a list of texts"""
        pass


class GoogleEmbeddingAdapter(EmbeddingAdapter):
    def __init__(self, model: str = "models/embedding-001"):  # 768 dim
        self.model = GoogleGenerativeAIEmbeddings(
            model=model,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

    async def embed(self, texts: List[str]) -> List[List[float]]:
        return await asyncio.to_thread(self.model.embed_documents, texts)


class LocalEmbeddingAdapter(EmbeddingAdapter):
    def __init__(self, model_name: str = "all-mpnet-base-v2"):  # 768 dim
        self.model = SentenceTransformer(model_name)

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return await asyncio.to_thread(self.model.encode, texts, show_progress_bar=False)


# lazy init of embedding adapter
_emb_adapter: EmbeddingAdapter | None = None


def get_emb_adapter(local: bool = False) -> EmbeddingAdapter:
    """Return a singleton embedding adapter using adapter pattern"""
    global _emb_adapter
    if _emb_adapter is None:
        _emb_adapter = LocalEmbeddingAdapter() if local else GoogleEmbeddingAdapter()
    return _emb_adapter
