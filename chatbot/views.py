import logging

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render
from django.views.decorators.http import require_POST

from contact.models import ContactMessage
from contact.notifications import notify_new_lead
from core.ratelimit import client_ip, is_rate_limited

from .gemini_client import ask_gemini

logger = logging.getLogger(__name__)

RATE_LIMITS = [
    ('burst', 3, 30),         # 3 messages / 30s par IP
    ('sustained', 30, 3600),  # 30 messages / heure par IP
]
MAX_HISTORY_MESSAGES = 16          # borne le coût/contexte envoyé à l'API
SESSION_KEY = 'chatbot_history'
VALID_SERVICE_TYPES = {choice for choice, _ in ContactMessage.SERVICE_CHOICES}


def _clean_email(raw_email):
    """Ne fait jamais confiance aveuglément à un champ produit par le LLM."""
    email = (raw_email or '').strip()[:254]
    try:
        validate_email(email)
    except ValidationError:
        return ''
    return email


def _save_lead(lead_data, transcript_excerpt):
    service_type = lead_data.get('service_type')
    if service_type not in VALID_SERVICE_TYPES:
        service_type = 'other'

    message = ContactMessage.objects.create(
        full_name=(lead_data.get('full_name') or 'Visiteur chatbot').strip()[:150],
        email=_clean_email(lead_data.get('email')),
        phone=(lead_data.get('phone') or '').strip()[:50],
        message=(lead_data.get('need_summary') or '').strip()[:2000],
        service_type=service_type,
        notes=f"Capturé automatiquement via le chatbot IA du site.\n\nExtrait de la conversation :\n{transcript_excerpt}",
    )
    notify_new_lead(message, source='Chatbot IA')


@require_POST
def send_message(request):
    ip = client_ip(request)
    user_message = (request.POST.get('message') or '').strip()

    if not user_message:
        return render(request, 'components/chatbot_messages.html', {'error': None})

    if is_rate_limited('chatbot_rl', ip, RATE_LIMITS):
        logger.warning('Chatbot rate-limited pour %s', ip)
        return render(request, 'components/chatbot_messages.html', {
            'user_message': user_message,
            'error': "Trop de messages envoyés. Merci de patienter quelques instants avant de continuer.",
        })

    history = request.session.get(SESSION_KEY, [])
    history.append({'role': 'user', 'content': user_message})

    try:
        reply_text, lead_data = ask_gemini(history[-MAX_HISTORY_MESSAGES:])
    except Exception:
        logger.exception('Appel Gemini échoué')
        return render(request, 'components/chatbot_messages.html', {
            'user_message': user_message,
            'error': "Désolé, une erreur technique est survenue. Réessaie dans un instant ou contacte Azeez directement.",
        })

    history.append({'role': 'assistant', 'content': reply_text})
    request.session[SESSION_KEY] = history[-MAX_HISTORY_MESSAGES:]

    if lead_data:
        transcript = '\n'.join(f"{m['role']}: {m['content']}" for m in history[-8:])
        try:
            _save_lead(lead_data, transcript)
        except Exception:
            logger.exception('Échec de la sauvegarde du lead chatbot')

    return render(request, 'components/chatbot_messages.html', {
        'user_message': user_message,
        'reply': reply_text,
        'error': None,
    })
