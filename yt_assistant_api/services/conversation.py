# conversation.py
from langchain.prompts import ChatPromptTemplate

from .llm_adapter import LLM, LLMOutputSize, get_adapter

# ===================================== PROMPT TEMPLATE =====================================

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a knowledgeable assistant specialized in explaining concepts 
            and answering questions about YouTube video content. 
            Be clear, concise, and structured. Use markdown when helpful, 
            and include code blocks or formulas if relevant. 
            Focus on technical accuracy and completeness, without unnecessary filler.""",
        ),
        (
            "human",
            """
            User question: {txt}

            Provide a helpful and concise answer.""",
        ),
    ]
)

# =================================== CONVERSATION ========================================


async def get_ai_response(user_message: str, model: LLM = LLM.GEMINI_2_0_FLASH) -> str:
    adapter = get_adapter(model, LLMOutputSize.M)
    return adapter.invoke({"txt": user_message}, chat_prompt)
