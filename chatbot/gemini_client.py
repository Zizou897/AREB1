import json
import re

from django.conf import settings
from google import genai
from google.genai import types

from .prompts import LEAD_BLOCK_PATTERN, SYSTEM_PROMPT

MODEL_NAME = 'gemini-3.5-flash-lite'

_client = None


def _get_client():
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError('GEMINI_API_KEY manquant dans la configuration.')
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def _to_gemini_role(role):
    return 'model' if role == 'assistant' else 'user'


def ask_gemini(history):
    """history : liste de {'role': 'user'|'assistant', 'content': str}, le dernier étant le nouveau message.

    Renvoie (reply_text, lead_data_or_none).
    """
    client = _get_client()
    *prior, last = history
    gemini_history = [
        types.Content(role=_to_gemini_role(m['role']), parts=[types.Part(text=m['content'])])
        for m in prior
    ]

    chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=500,
        ),
        history=gemini_history,
    )
    response = chat.send_message(last['content'])

    text = getattr(response, 'text', None)
    if not text:
        return "Désolé, je n'ai pas pu formuler de réponse. Peux-tu reformuler ta question ?", None

    lead_data = None
    match = re.search(LEAD_BLOCK_PATTERN, text, re.DOTALL)
    if match:
        text = text[:match.start()].strip()
        try:
            lead_data = json.loads(match.group(1))
        except (json.JSONDecodeError, TypeError):
            lead_data = None

    return text, lead_data
