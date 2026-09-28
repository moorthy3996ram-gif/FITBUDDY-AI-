import os
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv()

@lru_cache(maxsize=1)
def get_client():
    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key: return None
    try:
        from google import genai
        return genai.Client(api_key=key)
    except Exception:
        return None

def generate_text(prompt: str, model: str) -> str:
    client = get_client()
    if client is None: raise RuntimeError("Gemini API is not configured")
    response = client.models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if not text: raise RuntimeError("Gemini returned an empty response")
    return text.strip()

def model_name(kind: str) -> str:
    return os.getenv("GEMINI_PRO_MODEL" if kind == "pro" else "GEMINI_FLASH_MODEL",
                     "gemini-2.5-pro" if kind == "pro" else "gemini-2.5-flash")
