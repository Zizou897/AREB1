import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def notify_new_lead(message, source='Formulaire de contact'):
    """Notifie par email si un SMTP est configuré ; le message reste en base quoi qu'il arrive."""
    receiver = settings.CONTACT_RECEIVER_EMAIL
    if not receiver:
        return
    body = (
        f'Source : {source}\n'
        f'Nom : {message.full_name}\n'
        f'Email : {message.email}\n'
        f'Téléphone : {message.phone or "—"}\n\n'
        f'{message.message}'
    )
    try:
        send_mail(
            subject=f'[Portfolio] Nouveau message de {message.full_name}',
            message=body,
            from_email=settings.EMAIL_HOST_USER or 'portfolio@localhost',
            recipient_list=[receiver],
            fail_silently=False,
        )
    except Exception:
        logger.exception('Envoi email échoué (message #%s sauvegardé en base)', message.pk)
