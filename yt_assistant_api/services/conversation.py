# conversation.py
from langchain.prompts import ChatPromptTemplate

from .llm_adapter import LLM, LLMOutputSize, get_adapter

# ===================================== PROMPT TEMPLATE =====================================

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a knowledgeable assistant that explains technical concepts clearly and concisely.
            - Use markdown for formatting, should be rendering easily.
            - Include code blocks or LaTeX formulas when relevant.
            - Do NOT wrap math in square brackets `[...]` or parentheses `(...)` outside of proper LaTeX delimiters.
            - Focus on accuracy, clarity, and completeness without unnecessary filler.""",
        ),
        (
            "human",
            """
            User message: {txt}

            Provide a helpful and concise answer using markdown and LaTeX where needed.""",
        ),
    ]
)


# =================================== CONVERSATION ========================================


async def get_ai_response(user_message: str, model: LLM = LLM.GEMINI_2_0_FLASH) -> str:
    adapter = get_adapter(model, LLMOutputSize.L)
    return adapter.invoke({"txt": user_message}, chat_prompt)
