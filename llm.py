"""
Groq LLM Wrapper — Loads API key from .env, calls Groq for explanations only.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# Load .env from project root
load_dotenv(Path(__file__).parent / ".env")

_SYSTEM_PROMPT_PATH = Path(__file__).parent / "prompts" / "system_prompt.txt"
_SYSTEM_PROMPT = _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

_client: Groq | None = None

MODEL = "llama-3.3-70b-versatile"


def _get_client() -> Groq:
    """Lazily initialize the Groq client."""
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GROQ_API_KEY not found. Add it to your .env file or Streamlit secrets."
            )
        _client = Groq(api_key=api_key)
    return _client


def get_llm_explanation(user_query: str, tool_outputs: str) -> str:
    """
    Send tool outputs + user context to Groq LLM and get a human-friendly explanation.

    Args:
        user_query: The original user question.
        tool_outputs: Formatted string of deterministic tool results.

    Returns:
        LLM-generated explanation string.
    """
    client = _get_client()

    user_message = (
        f"User Question: {user_query}\n\n"
        f"Tool Results (use these numbers exactly, do NOT recompute):\n{tool_outputs}"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.4,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Could not generate explanation: {e}"
