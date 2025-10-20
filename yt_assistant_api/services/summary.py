from langchain.prompts import ChatPromptTemplate

from .llm_adapter import LLM, LLMOutputSize, get_adapter

# ===================================== PROMPT TEMPLATE =====================================

summarization_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a technical assistant that makes concise, structured study notes."
            "Keep only core knowledge — definitions, theorems, formulas, concepts, and key insights."
            "Exclude intros, anecdotes, and filler. Preserve technical details."
            "Write equations and expressions explicitly (e.g., using LaTeX-style or code blocks)."
            "Use markdown: subheadings (##, ### or ####), bullet points etc."
            "No title."
            "The output should look like high-quality lecture notes written by a top student."
            "Ensure the output is complete and ends with a full sentence or section.",
        ),
        ("human", "Summarize the following content:\n\n{txt}\n\n"),
    ]
)


# =================================== SUMMARIZE ========================================


def get_summary_size(txt: str) -> LLMOutputSize:
    n = len(txt)
    if n < 1000:
        return LLMOutputSize.S
    if n < 3000:
        return LLMOutputSize.M
    return LLMOutputSize.L


def summarize(txt: str, model: LLM = LLM.GEMINI_2_0_FLASH) -> str:
    """
    Summarize input text using the selected model and appropriate output size.
    """
    size = get_summary_size(txt)
    adapter = get_adapter(model, size)
    return adapter.invoke(txt, summarization_prompt)
