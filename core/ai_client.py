import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from core import config

load_dotenv()


class AIError(Exception):
    """Error with a simple message that is safe to show to the user."""


_client = None


def _get_client():
    global _client
    if _client is None:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise AIError("API key is missing. Please set GEMINI_API_KEY.")
        _client = genai.Client(api_key=key)
    return _client


def ask_ai(prompt, system_instruction=None):
    """Send a prompt to Gemini and return the answer text.

    Tries the main model first. If it is busy, retries, then moves
    to the next backup model. Raises AIError with a friendly message.
    """
    if not prompt or not prompt.strip():
        raise AIError("Please enter some text first.")

    client = _get_client()
    cfg = None
    if system_instruction:
        cfg = types.GenerateContentConfig(system_instruction=system_instruction)

    for model in config.MODEL_CANDIDATES:
        for attempt in range(config.MAX_RETRIES_PER_MODEL):
            try:
                response = client.models.generate_content(
                    model=model, contents=prompt, config=cfg
                )
                if response.text:
                    return response.text
                break  # empty answer: try the next model
            except errors.APIError as e:
                code = getattr(e, "code", None)
                if code in (500, 503, 504):
                    # server busy: wait a bit and try again
                    time.sleep(config.RETRY_WAIT_SECONDS * (attempt + 1))
                    continue
                if code in (429, 404):
                    break  # limit reached or model closed: next model
                if code in (400, 401, 403):
                    raise AIError("API key problem. Please check your key.")
                raise AIError("The AI returned an error. Please try again.")
            except Exception:
                raise AIError("Could not reach the AI. Check your internet.")

    raise AIError("The AI is busy right now. Please try again in a minute.")