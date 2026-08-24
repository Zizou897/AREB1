"""Témoignages placeholder — noms réels à renseigner via l'admin Django."""

from django.db import migrations

SEED = [
    {
        'author_name': 'Client à renseigner',
        'author_title': 'Gérant, PME Abidjan',
        'content': (
            'Azeez a livré notre application dans les délais, exactement comme prévu. '
            'Le résultat dépasse nos attentes — notre équipe a adopté l’outil en moins '
            'd’une semaine.'
        ),
        'featured': True,
    },
    {
        'author_name': 'Client à renseigner',
        'author_title': 'Responsable marketing, startup tech',
        'content': (
            'La vidéo publicitaire IA qu’il a créée pour notre lancement a généré '
            'un engagement exceptionnel sur nos réseaux. Qualité pro, délai express.'
        ),
        'featured': True,
    },
]


def seed(apps, schema_editor):
    Testimonial = apps.get_model('testimonials', 'Testimonial')
    for entry in SEED:
        Testimonial.objects.create(**entry)


def unseed(apps, schema_editor):
    Testimonial = apps.get_model('testimonials', 'Testimonial')
    Testimonial.objects.filter(author_name='Client à renseigner').delete()


class Migration(migrations.Migration):
    dependencies = [('testimonials', '0001_initial')]
    operations = [migrations.RunPython(seed, unseed)]
