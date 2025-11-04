import asyncio
from abc import ABC, abstractmethod
from enum import Enum, IntEnum

from config import settings
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


class LLM(Enum):
    GEMINI_2_0_FLASH = "gemini-2.0-flash"


# =================================== LLM ADAPTER =======================================
class LLMAdapter(ABC):
    @abstractmethod
    async def invoke(self, txt: str, prompt: ChatPromptTemplate) -> str:
        pass


class GeminiAdapter(LLMAdapter):
    def __init__(self, max_tokens: int, model: LLM = LLM.GEMINI_2_0_FLASH):
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.1,
            max_tokens=max_tokens,
            max_retries=1,
        )

    async def invoke(self, txt: str, prompt: ChatPromptTemplate, context: str = '') -> str:
        return await asyncio.to_thread(self._invoke_sync, txt, prompt, context)

    def _invoke_sync(self, txt: str, prompt: ChatPromptTemplate, context: str) -> str:
        messages = prompt.format_messages(txt=txt, context=context)
        result = self.llm.invoke(
            messages
        )  # LangChain ChatGoogleGenerativeAI.invoke does not support async
        return result.content


# ================================ LLM OUTPUT SIZE =====================================
class LLMOutputSize(IntEnum):
    S = 256
    M = 512
    L = 1024


# ============================= LAZY ADAPTER REGISTRY ==================================


_ADAPTERS: dict[tuple[LLM, LLMOutputSize], LLMAdapter] = {}


def get_adapter(model: LLM, max_tokens: LLMOutputSize) -> LLMAdapter:
    key = (model, max_tokens)
    if key not in _ADAPTERS:
        if model in [LLM.GEMINI_2_0_FLASH]:
            _ADAPTERS[key] = GeminiAdapter(max_tokens, model)
        else:
            raise ValueError(f"Unsupported model type: {model}")
    return _ADAPTERS[key]
