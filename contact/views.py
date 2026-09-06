import logging

from django.shortcuts import render
from django.views.decorators.http import require_POST

from core.ratelimit import client_ip, is_rate_limited

from .forms import ContactForm
from .notifications import notify_new_lead

logger = logging.getLogger(__name__)

# Rate limiting du formulaire : une fenêtre courte contre le double-clic / les bots
# rapides, une fenêtre longue contre les campagnes de spam soutenues.
RATE_LIMITS = [
    ('burst', 1, 30),        # 1 envoi / 30 secondes par IP
    ('sustained', 5, 3600),  # 5 envois / heure par IP
]


@require_POST
def submit(request):
    """Soumission HTMX : renvoie le partial succès (ou le formulaire avec erreurs)."""
    ip = client_ip(request)
    if is_rate_limited('contact_rl', ip, RATE_LIMITS):
        logger.warning('Contact rate-limited pour %s', ip)
        form = ContactForm(request.POST)
        form.is_valid()
        form.add_error(None, 'Trop de tentatives. Merci de réessayer dans quelques minutes.')
        return render(request, 'components/contact_form.html', {'contact_form': form}, status=429)

    form = ContactForm(request.POST)
    if not form.is_valid():
        return render(request, 'components/contact_form.html', {'contact_form': form})

    if form.cleaned_data.get('website'):
        # Honeypot rempli : quasi certainement un bot. On simule un succès sans
        # rien sauvegarder ni notifier, pour ne pas révéler le piège.
        logger.info('Contact honeypot déclenché pour %s', ip)
        return render(request, 'components/contact_success.html', {
            'first_name': form.cleaned_data.get('full_name', '').split()[0] or 'là',
        })

    message = form.save()
    notify_new_lead(message)
    return render(request, 'components/contact_success.html', {
        'first_name': message.full_name.split()[0],
    })
