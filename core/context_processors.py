from django.conf import settings
from django.urls import translate_url

from .models import SiteSettings
from .translations import get_translation


def site_info(request):
    current_lang = 'en' if request.LANGUAGE_CODE.startswith('en') else 'fr'
    other_lang = 'fr' if current_lang == 'en' else 'en'
    t = get_translation(current_lang)

    return {
        'site': SiteSettings.load(),
        'current_lang': current_lang,
        'other_lang': other_lang,
        't': t,
        'site_url': settings.SITE_URL,
        'canonical_url': f'{settings.SITE_URL}{request.path}',
        'lang_switch_url_fr': translate_url(request.path, 'fr'),
        'lang_switch_url_en': translate_url(request.path, 'en'),
    }
