"""Pré-remplit les 3 projets de vidéo IA publicitaire (brief, outils IA, secteur)
en copiant les miniatures vers MEDIA_ROOT/projects/."""

import shutil
from pathlib import Path

from django.conf import settings
from django.db import migrations

VIDEO_PROJECTS = [
    {
        'title': 'L’Atelier Gourmand — Spot Publicitaire Gastronomie',
        'category': 'video',
        'sector': 'Restauration & Food',
        'description': (
            'Campagne publicitaire vidéo 100% générée par IA pour un établissement '
            'gastronomique haut de gamme. Conception visuelle des plats signatures, '
            'dynamique de caméra cinématique et sound design immersif.'
        ),
        'problem': (
            'Le restaurant souhaitait lancer sa nouvelle carte avec une vidéo publicitaire '
            'de qualité cinéma sans immobiliser les cuisines pour un tournage coûteux.'
        ),
        'solution': (
            'Génération des plans de coupe culinaires avec Runway Gen-3 et Kling AI, '
            'voix off chaleureuse via ElevenLabs, et étalonnage couleur studio.'
        ),
        'result': (
            '+140% d’engagement sur les réseaux sociaux lors du lancement et réservations '
            'complètes sur les 3 premiers week-ends.'
        ),
        'stack': ['Runway Gen-3', 'Kling AI', 'ElevenLabs', 'Adobe Firefly', 'CapCut AI'],
        'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'thumbnail_file': 'video_atelier_gourmand.webp',
        'featured': True,
        'order': 4,
    },
    {
        'title': 'Aura Luxury Timepieces — Campagne E-Commerce',
        'category': 'video',
        'sector': 'E-Commerce Horlogerie',
        'description': (
            'Spot publicitaire 3D cinématique pour le lancement d’un chronographe de luxe. '
            'Mise en valeur macro du mécanisme squelette, textures titane et apesanteur.'
        ),
        'problem': (
            'Une marque D2C avait besoin d’un spot percutant pour ses campagnes publicitaires Meta & TikTok '
            'avec un rendu CGI de niveau mondial dans un délai de 5 jours.'
        ),
        'solution': (
            'Direction artistique et génération de mouvements d’orbite 3D avec Midjourney et Runway, '
            'effets volumétriques et montage dynamique optimisé pour les formats verticaux et horizontaux.'
        ),
        'result': (
            'Taux de conversion publicitaire (ROAS) de 3.8x dès la première semaine de diffusion.'
        ),
        'stack': ['Midjourney v6', 'Runway ML', 'Adobe Premiere Pro', 'CapCut AI'],
        'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'thumbnail_file': 'video_aura_timepieces.webp',
        'featured': True,
        'order': 5,
    },
    {
        'title': 'NeoHabitat — Concept Architecture & Résidences',
        'category': 'video',
        'sector': 'Immobilier & Architecture',
        'description': (
            'Présentation cinématique d’un projet de villas contemporaines en bord de mer. '
            'Transitions jour/nuit photoréalistes et ambiance sonore architecturale.'
        ),
        'problem': (
            'Les promoteurs devaient commercialiser le programme immobilier avant même le début du chantier '
            'avec des visuels animés ultra-réalistes et séduisants.'
        ),
        'solution': (
            'Modélisation générative des espaces de vie et de la piscine à débordement avec Kling AI et Pika Labs, '
            'voix off narrative multilingue avec ElevenLabs.'
        ),
        'result': (
            '70% des lots réservés lors de la phase de pré-commercialisation.'
        ),
        'stack': ['Kling AI', 'Pika Labs', 'ElevenLabs', 'Runway ML'],
        'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'thumbnail_file': 'video_neohabitat.webp',
        'featured': False,
        'order': 6,
    },
]


def seed_video_projects(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    static_dir = Path(settings.BASE_DIR) / 'static' / 'img' / 'projects'
    media_dir = Path(settings.MEDIA_ROOT) / 'projects'
    media_dir.mkdir(parents=True, exist_ok=True)

    for entry in VIDEO_PROJECTS:
        thumb_file = entry.pop('thumbnail_file')
        src = static_dir / thumb_file
        dest = media_dir / thumb_file
        thumbnail_path = f'projects/{thumb_file}'
        if src.exists() and not dest.exists():
            shutil.copy2(src, dest)
        Project.objects.create(thumbnail=thumbnail_path, **entry)


def unseed_video_projects(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    Project.objects.filter(title__in=[e['title'] for e in VIDEO_PROJECTS]).delete()


class Migration(migrations.Migration):
    dependencies = [('projects', '0002_seed_projects')]
    operations = [migrations.RunPython(seed_video_projects, unseed_video_projects)]
