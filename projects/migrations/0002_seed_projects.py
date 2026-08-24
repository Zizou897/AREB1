"""Pré-remplit les 3 projets web (contenu : portfolio_content.md) en copiant
les screenshots capturés depuis static/img/projects/ vers MEDIA_ROOT/projects/."""

import shutil
from pathlib import Path

from django.conf import settings
from django.db import migrations

SEED = [
    {
        'title': 'CTAMS — Système de gestion associative',
        'category': 'web',
        'description': (
            'Plateforme web complète de gestion pour organisations et associations. '
            'Gestion des membres, des cotisations, des événements et des rapports.'
        ),
        'problem': (
            'Les associations géraient leurs données sur Excel, sans centralisation '
            'ni accès multi-utilisateurs, ce qui causait des erreurs et des pertes de données.'
        ),
        'solution': (
            'Développement d’une application Django full-featured avec authentification '
            'multi-rôles, tableau de bord en temps réel, gestion des cotisations '
            'et export de rapports PDF.'
        ),
        'result': (
            'Adoption par plusieurs associations. Réduction du temps de gestion '
            'administrative de 60%. Accès centralisé pour tous les membres depuis '
            'n’importe quel appareil.'
        ),
        'stack': ['Python', 'Django', 'PostgreSQL', 'Bootstrap', 'JavaScript'],
        'live_url': 'https://www.ctams.net',
        'screenshot': 'ctams_desktop.webp',
        'featured': True,
        'order': 1,
    },
    {
        'title': 'MonApplideGestion — Application de gestion PME',
        'category': 'web',
        'description': (
            'Application SaaS de gestion commerciale pour PME africaines. '
            'Gestion des ventes, stocks, clients et facturation.'
        ),
        'problem': (
            'Les PME locales n’avaient pas accès à des outils de gestion adaptés '
            'à leur contexte (multi-devises, faible bande passante) et abordables.'
        ),
        'solution': (
            'Développement d’une app Django légère et responsive, optimisée pour '
            'les connexions lentes, avec gestion des devis, factures, stocks et clients.'
        ),
        'result': (
            'Outil utilisé activement par des PME de la région. '
            'Interface rapide même sur réseau mobile 3G.'
        ),
        'stack': ['Python', 'Django', 'SQLite / PostgreSQL', 'HTMX', 'TailwindCSS'],
        'live_url': 'https://monapplidegestion.online',
        'screenshot': 'monappligestion_online_desktop.webp',
        'featured': False,
        'order': 2,
    },
    {
        'title': 'MonApplideGestion — Version entreprise',
        'category': 'web',
        'description': (
            'Version étendue de l’application de gestion, avec des fonctionnalités '
            'avancées pour les entreprises : multi-utilisateurs, rôles, rapports avancés.'
        ),
        'problem': (
            'Les entreprises plus grandes avaient besoin de plus de contrôle : '
            'gestion d’équipe, audit trail, et tableaux de bord analytiques.'
        ),
        'solution': (
            'Extension de l’architecture Django avec API FastAPI pour les modules '
            'analytiques, système de rôles granulaire, et exports Excel/PDF automatisés.'
        ),
        'result': 'Déployé en production. Architecture scalable prête pour la montée en charge.',
        'stack': ['Python', 'Django', 'FastAPI', 'PostgreSQL', 'Chart.js', 'HTMX'],
        'live_url': 'https://monapplidegestion.net',
        'screenshot': 'monappligestion_net_desktop.webp',
        'featured': False,
        'order': 3,
    },
]


def seed(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    static_dir = Path(settings.BASE_DIR) / 'static' / 'img' / 'projects'
    media_dir = Path(settings.MEDIA_ROOT) / 'projects'
    media_dir.mkdir(parents=True, exist_ok=True)

    for entry in SEED:
        screenshot = entry.pop('screenshot')
        src = static_dir / screenshot
        thumbnail = ''
        if src.exists():
            shutil.copy2(src, media_dir / screenshot)
            thumbnail = f'projects/{screenshot}'
        Project.objects.create(thumbnail=thumbnail, **entry)


def unseed(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    Project.objects.filter(title__in=[e['title'] for e in SEED]).delete()


class Migration(migrations.Migration):
    dependencies = [('projects', '0001_initial')]
    operations = [migrations.RunPython(seed, unseed)]
