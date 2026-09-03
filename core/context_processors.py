from django.conf import settings

from .models import SiteSettings
from .translations import get_translation


def site_info(request):
    # Langue demandée par paramètre d'URL, session, cookie ou en-tête
    lang = request.GET.get('lang')
    if lang in ('fr', 'en'):
        if hasattr(request, 'session'):
            request.session['django_language'] = lang
    else:
        lang = getattr(request, 'session', {}).get('django_language') if hasattr(request, 'session') else None
        if not lang:
            lang = request.COOKIES.get('django_language')
        if not lang and hasattr(request, 'LANGUAGE_CODE'):
            lang = 'en' if request.LANGUAGE_CODE.startswith('en') else 'fr'
        if not lang:
            lang = 'fr'

    current_lang = 'en' if lang.startswith('en') else 'fr'
    other_lang = 'fr' if current_lang == 'en' else 'en'
    t = get_translation(current_lang)

    return {
        'site': SiteSettings.load(),
        'current_lang': current_lang,
        'other_lang': other_lang,
        't': t,
        'site_url': settings.SITE_URL,
        'canonical_url': f'{settings.SITE_URL}{request.path}',
    }
