"""Pré-remplit SiteSettings depuis settings.SITE_INFO (.env) et les Skills
depuis l'ancien core/data.py, pour que rien ne change visiblement sur le site
au moment du passage à un contenu piloté par la base de données."""

from django.conf import settings
from django.db import migrations

SKILLS_DEV = [
    {'name': 'Python', 'level': 'Expert'},
    {'name': 'Django', 'level': 'Expert'},
    {'name': 'API REST', 'level': 'Expert'},
    {'name': 'FastAPI', 'level': 'Avancé'},
    {'name': 'HTMX', 'level': 'Avancé'},
    {'name': 'PostgreSQL', 'level': 'Avancé'},
    {'name': 'Git / GitHub', 'level': 'Avancé'},
    {'name': 'TailwindCSS', 'level': 'Intermédiaire'},
    {'name': 'Linux / Déploiement', 'level': 'Intermédiaire'},
]

SKILLS_VIDEO = [
    {'name': 'Runway ML', 'usage': 'Génération vidéo IA'},
    {'name': 'Kling AI', 'usage': 'Animation et vidéo'},
    {'name': 'ElevenLabs', 'usage': 'Voix off IA'},
    {'name': 'Sora', 'usage': 'Génération vidéo'},
    {'name': 'Pika Labs', 'usage': 'Animation'},
    {'name': 'CapCut AI', 'usage': 'Montage assisté IA'},
    {'name': 'Adobe Firefly', 'usage': 'Visuels IA'},
]


def seed(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    Skill = apps.get_model('core', 'Skill')

    info = settings.SITE_INFO
    SiteSettings.objects.get_or_create(pk=1, defaults={
        'name': info.get('name', 'Azeez Ridwan'),
        'email': info.get('email', 'contact@azeezridwan.com'),
        'whatsapp': info.get('whatsapp', ''),
        'telegram': info.get('telegram', ''),
        'linkedin': info.get('linkedin', ''),
        'github': info.get('github', ''),
        'location': info.get('location', 'Abidjan, Côte d’Ivoire'),
        'available': True,
    })

    for order, entry in enumerate(SKILLS_DEV):
        Skill.objects.get_or_create(
            name=entry['name'], category='dev',
            defaults={'detail': entry['level'], 'order': order},
        )
    for order, entry in enumerate(SKILLS_VIDEO):
        Skill.objects.get_or_create(
            name=entry['name'], category='video',
            defaults={'detail': entry['usage'], 'order': order},
        )


def unseed(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    Skill = apps.get_model('core', 'Skill')
    SiteSettings.objects.filter(pk=1).delete()
    names = [e['name'] for e in SKILLS_DEV] + [e['name'] for e in SKILLS_VIDEO]
    Skill.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]
    operations = [migrations.RunPython(seed, unseed)]
