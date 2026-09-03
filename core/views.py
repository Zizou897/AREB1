from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from contact.forms import ContactForm
from projects.models import Project
from testimonials.models import Testimonial

from .models import Skill, SiteSettings


def home(request):
    all_projects = Project.objects.all()
    skills_video = list(Skill.objects.filter(category='video'))

    site = SiteSettings.load()
    showcase_videos = [v for v in (site.showcase_video_1, site.showcase_video_2) if v]

    MIN_TEASER_COUNT = 2
    featured_projects = list(all_projects.filter(featured=True))
    if len(featured_projects) < MIN_TEASER_COUNT:
        seen_ids = {p.pk for p in featured_projects}
        for project in all_projects:
            if len(featured_projects) >= max(MIN_TEASER_COUNT, 3):
                break
            if project.pk not in seen_ids:
                featured_projects.append(project)
                seen_ids.add(project.pk)

    context = {
        'active_category': 'all',
        'featured_projects': featured_projects,
        'ai_tools': [skill.name for skill in skills_video],
        'skills_dev': Skill.objects.filter(category='dev'),
        'skills_video': skills_video,
        'testimonials': Testimonial.objects.all(),
        'contact_form': ContactForm(),
        'flagship_video': showcase_videos[0] if showcase_videos else None,
        'spotlight_videos': showcase_videos[1:],
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


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Disallow: /dashboard/',
        'Disallow: /admin/',
        '',
        f'Sitemap: {settings.SITE_URL}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)

