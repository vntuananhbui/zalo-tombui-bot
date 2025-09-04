import os
from typing import Optional
from langdetect import detect
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv(".env")

def _detect_language_hint(text: str) -> str:
    # Use langdetect to detect language; fall back to 'auto' on failure
    try:
        if not text or not text.strip():
            return "auto"
        return detect(text)
    except Exception:
        return "auto"


async def generate_reply(user_text: str, user_locale: Optional[str] = None) -> str:
    """
    Generate a response using OpenAI via LangChain. The reply should be in the user's language.
    If user_locale is provided, use it; otherwise attempt a best-effort auto-detection.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY is not set on the server."

    # Determine target language code or instruction
    language_hint = (user_locale or "").strip() or _detect_language_hint(user_text)

    # Build LLM and messages
    llm = ChatOpenAI(
        model="gpt-4.1",
        temperature=0.7,
        openai_api_key=api_key,
    )
    system_prompt = (
        "You are a chatbot Powered by TuanAnh. Always reply in the user's language. "
        f"If a language hint exists, prefer it. Language hint: {language_hint}."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_text or ""),
    ]

    try:
        result = await llm.ainvoke(messages)
        return result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        # Common causes: wrong OPENAI_BASE_URL, DNS/Proxy issues, network down
        print(f"LLM error: {e}")
        return f"LLM error: {e}"
