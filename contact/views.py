import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import ContactForm

logger = logging.getLogger(__name__)


@require_POST
def submit(request):
    """Soumission HTMX : renvoie le partial succès (ou le formulaire avec erreurs)."""
    form = ContactForm(request.POST)
    if not form.is_valid():
        return render(request, 'components/contact_form.html', {'contact_form': form})

    message = form.save()
    _notify(message)
    return render(request, 'components/contact_success.html', {
        'first_name': message.full_name.split()[0],
    })


def _notify(message):
    """Notifie par email si un SMTP est configuré ; le message reste en base quoi qu'il arrive."""
    receiver = settings.CONTACT_RECEIVER_EMAIL
    if not receiver:
        return
    body = (
        f'Nom : {message.full_name}\n'
        f'Email : {message.email}\n\n'
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
        logger.exception('Envoi email contact échoué (message #%s sauvegardé en base)', message.pk)
