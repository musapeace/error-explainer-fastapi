# app/analyzer.py
import os
import asyncio
from dotenv import load_dotenv
 

load_dotenv()

from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")

client = genai.Client(api_key=GEMINI_API_KEY) 

SYSTEM_PROMPT = ("You are Error Explainer Agent. Given a program error message or stacktrace, "
    "produce a concise, human-friendly explanation of what went wrong, the likely root cause(s), "
    "and 2-3 practical steps to fix or debug it. Keep the explanation short (max ~200 words).")

async def get_error_explanation(error_message: str) -> str:
    """ Send the error message to the LLM synchronously via a thread so this function remains async.
    Use defensive parsing for the response payload because different SDK versions return different shapes."""


    if not error_message:
        return "No error message provided."

    # Prepare content for the model (adapt this if your genai SDK expects different fields)
    contents = [
        {"role": "system", "text": SYSTEM_PROMPT},
        {"role": "user", "text": error_message}
    ]

    try:
        # Run blocking call in a background thread so we don't block the event loop
        result = await asyncio.to_thread(
            lambda: client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents
            )
        )
    except Exception as e:

        return f"Error: Could not process request with LLM. Details: {type(e).__name__}: {str(e)}"

    # Defensive extraction of text from the result object
    try:
        # Many SDKs expose .text
        if hasattr(result, "text") and isinstance(result.text, str):
            return result.text.strip()

        # Some return .output or .outputs
        if hasattr(result, "output"):
            out = getattr(result, "output")
            # Try to join text from possible nested content
            if isinstance(out, str):
                return out.strip()
            if isinstance(out, (list, tuple)):
                parts = []
                for item in out:
                    text = item.get("content") if isinstance(item, dict) else None
                    if not text and isinstance(item, dict):
                        text = item.get("text") or item.get("message") or None
                    if text:
                        parts.append(text)
                if parts:
                    return "\n".join(parts).strip()

        # Try attribute 'outputs'
        if hasattr(result, "outputs"):
            outs = getattr(result, "outputs")
            if isinstance(outs, (list, tuple)) and len(outs) > 0:
                # attempt several common keys
                candidate = outs[0]
                if isinstance(candidate, dict):
                    for k in ("content", "text", "message"):
                        if k in candidate:
                            return candidate[k].strip()
        # Last resort: string representation
        return str(result)[:2000]
    except Exception:
        # Fall back - avoid raising further
        return "Received an unexpected response from the LLM." 