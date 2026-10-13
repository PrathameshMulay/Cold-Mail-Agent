import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm(api_key: str | None = None):
    # An explicitly supplied user key takes priority.
    resolved_api_key = (
        api_key or os.getenv("GEMINI_API_KEY") or ""
    ).strip()

    if not resolved_api_key:
        raise ValueError("A Gemini API key is required.")

    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        google_api_key=resolved_api_key,
        temperature=0,
        max_retries=2,
    )
