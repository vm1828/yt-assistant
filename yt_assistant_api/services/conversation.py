from langchain.prompts import ChatPromptTemplate
from models import Conversation

from .llm_adapter import LLM, LLMOutputSize, get_adapter

# ===================================== PROMPT TEMPLATES =====================================

rag_judge_prompt = ChatPromptTemplate.from_template(
    """
    You are classifying whether the following user message requires the current video context to answer.

    Message: "{txt}"

    Answer only "YES" or "NO".
    """
)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant helping the user understand and talk about the YouTube video they’re currently watching or asking about.
            - Keep responses concise, natural, and relevant — sound like you're talking to the user, not writing a report.
            - Respond conversationally, using markdown, LaTeX, and code if relevant.
            - Include code blocks or LaTeX formulas when appropriate.
            - Do NOT output full context dumps or irrelevant transcript parts.
            - Focus on what directly helps the user understand or solve the current question.
            - If the user’s question can be answered without using context, ignore the context.
            - Maintain clarity and precision while staying conversational.""",
        ),
        (
            "human",
            """
            User message: {{txt}}

            {% if context %}
            Some related video transcript snippets:
            ---
            {{context}}
            ---
            {% endif %}
            """,
        ),
    ],
    template_format="jinja2",
)


# =================================== CONVERSATION ========================================


def get_user_msg_w_history(user_message: str, conversation: Conversation) -> str:
    history = []
    for msg in conversation.messages:
        history.append(f"User: {msg.user_message}")
        history.append(f"Assistant: {msg.ai_response}")
    history.append(f"User: {user_message}")
    return "\n".join(history)


async def should_use_context(user_msg: str, model: LLM = LLM.GEMINI_2_0_FLASH) -> bool:
    adapter = get_adapter(model, LLMOutputSize.L)
    result = await adapter.invoke(user_msg, rag_judge_prompt)
    return result == "YES"


async def get_ai_response(
    user_msg_w_history: str, context: str, model: LLM = LLM.GEMINI_2_0_FLASH
) -> str:
    adapter = get_adapter(model, LLMOutputSize.L)
    return await adapter.invoke(user_msg_w_history, chat_prompt, context)
