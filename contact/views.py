import logging

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import ContactForm

logger = logging.getLogger(__name__)

# Rate limiting du formulaire : une fenêtre courte contre le double-clic / les bots
# rapides, une fenêtre longue contre les campagnes de spam soutenues.
RATE_LIMIT_BURST = (1, 30)       # 1 envoi / 30 secondes par IP
RATE_LIMIT_SUSTAINED = (5, 3600)  # 5 envois / heure par IP


def _client_ip(request):
    """IP réelle du visiteur derrière le reverse proxy Nginx (X-Real-IP)."""
    forwarded = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def _is_rate_limited(ip):
    """Incrémente les compteurs et renvoie True si l'une des limites est dépassée."""
    for label, (limit, window) in (('burst', RATE_LIMIT_BURST), ('sustained', RATE_LIMIT_SUSTAINED)):
        key = f'contact_rl_{label}_{ip}'
        count = cache.get(key)
        if count is None:
            cache.set(key, 1, timeout=window)
        elif count >= limit:
            return True
        else:
            cache.incr(key)
    return False


@require_POST
def submit(request):
    """Soumission HTMX : renvoie le partial succès (ou le formulaire avec erreurs)."""
    ip = _client_ip(request)
    if _is_rate_limited(ip):
        logger.warning('Contact rate-limited pour %s', ip)
        form = ContactForm(request.POST)
        form.is_valid()
        form.add_error(None, 'Trop de tentatives. Merci de réessayer dans quelques minutes.')
        return render(request, 'components/contact_form.html', {'contact_form': form}, status=429)

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
