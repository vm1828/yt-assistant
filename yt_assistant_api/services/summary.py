import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0.1,
    max_tokens=500,
    max_retries=1,
)

from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a technical assistant that converts dense content into concise, structured study notes.",
        ),
        (
            "human",
            "Summarize the following content:\n\n{text}\n\n"
            "Keep only core knowledge — definitions, theorems, formulas, concepts, and key insights. "
            "Exclude intros, anecdotes, and filler. Preserve technical details."
            "Write equations and expressions explicitly (e.g., using LaTeX-style or code blocks)."
            "Use markdown: headings (##), subheadings (### or ####), bullet points, and fenced code blocks for math or code."
            "Ensure the output is complete and ends with a full sentence or section."
            "The output should look like high-quality lecture notes written by a top student.",
        ),
    ]
)


def summarize(txt: str) -> str:
    messages = prompt.format_messages(text=txt)
    response = llm(messages)

    return response.content
