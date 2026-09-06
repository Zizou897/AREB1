import logging

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


def _save_lead(lead_data, transcript_excerpt):
    message = ContactMessage.objects.create(
        full_name=lead_data.get('full_name', 'Visiteur chatbot'),
        email=lead_data.get('email', ''),
        phone=lead_data.get('phone', ''),
        message=lead_data.get('need_summary', ''),
        service_type=lead_data.get('service_type') or 'other',
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
