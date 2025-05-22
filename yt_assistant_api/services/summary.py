import os
from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# ===================================== PROMPT TEMPLATE =====================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a technical assistant that converts dense content into concise, structured study notes.",
        ),
        (
            "human",
            "Summarize the following content:\n\n{txt}\n\n"
            "Keep only core knowledge — definitions, theorems, formulas, concepts, and key insights."
            "Exclude intros, anecdotes, and filler. Preserve technical details."
            "Write equations and expressions explicitly (e.g., using LaTeX-style or code blocks)."
            "Use markdown: subheadings (##, ### or ####), bullet points etc."
            "No title."
            "The output should look like high-quality lecture notes written by a top student."
            "Ensure the output is complete and ends with a full sentence or section.",
        ),
    ]
)


# ===================================== SUMMARY SIZE ========================================
class SumSize(IntEnum):
    S = 256
    M = 512
    L = 1024


def get_summary_size(txt: str) -> SumSize:
    n = len(txt)
    if n < 500:
        return SumSize.S
    if n < 2000:
        return SumSize.M
    return SumSize.L


# ============================= SUMMARIZATION MODEL ADAPTER ==================================
class LLMAdapter(ABC):
    @abstractmethod
    def summarize(self, txt: str) -> str:
        pass


class GeminiAdapter(LLMAdapter):
    def __init__(self, max_tokens: int):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.environ["GOOGLE_API_KEY"],
            temperature=0.1,
            max_tokens=max_tokens,
            max_retries=1,
        )

    def summarize(self, txt: str) -> str:
        messages = prompt.format_messages(txt=txt)
        result = self.llm.invoke(messages)
        return result.content


# ============================= LAZY ADAPTER REGISTRY ==================================


class SumModel(Enum):
    GEMINI = "gemini"


_ADAPTERS: dict[tuple[SumModel, SumSize], LLMAdapter] = {}


def get_adapter(model: SumModel, size: SumSize) -> LLMAdapter:
    key = (model, size)
    if key not in _ADAPTERS:
        if model == SumModel.GEMINI:
            _ADAPTERS[key] = GeminiAdapter(size)
        else:
            raise ValueError(f"Unsupported model type: {model}")
    return _ADAPTERS[key]


# =================================== SUMMARIZE ========================================


def summarize(txt: str, model: SumModel = SumModel.GEMINI) -> str:
    """
    Summarize input text using the selected model and appropriate output size.
    """
    size = get_summary_size(txt)
    adapter = get_adapter(model, size)
    return adapter.summarize(txt)
