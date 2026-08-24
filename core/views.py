from django.http import HttpResponseRedirect
from django.shortcuts import render

from contact.forms import ContactForm
from projects.models import AI_TOOLS, Project
from testimonials.models import Testimonial

from .data import SKILLS_DEV, SKILLS_VIDEO


def home(request):
    context = {
        'projects': Project.objects.all(),
        'active_category': 'all',
        'ai_tools': AI_TOOLS,
        'skills_dev': SKILLS_DEV,
        'skills_video': SKILLS_VIDEO,
        'testimonials': Testimonial.objects.all(),
        'contact_form': ContactForm(),
    }
    return render(request, 'pages/home.html', context)


def set_language(request, lang_code):
    """Bascule la langue active (fr / en) et redirige vers la page précédente."""
    lang = 'en' if str(lang_code).lower().startswith('en') else 'fr'
    referer = request.META.get('HTTP_REFERER') or '/'
    response = HttpResponseRedirect(referer)
    if hasattr(request, 'session'):
        request.session['django_language'] = lang
    response.set_cookie('django_language', lang, max_age=365 * 24 * 60 * 60, samesite='Lax')
    return response


def legal(request):
    return render(request, 'pages/legal.html')


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)

