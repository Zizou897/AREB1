from django.db import models


class SiteSettings(models.Model):
    """Réglages globaux du site (coordonnées, réseaux, disponibilité).

    Instance unique — voir `load()`. Remplace les valeurs figées dans .env
    pour que tout soit pilotable depuis l'admin sans redéploiement.
    """
    name = models.CharField('Nom affiché', max_length=100, default='Azeez Ridwan')
    email = models.EmailField('Email de contact')
    whatsapp = models.CharField('Numéro WhatsApp', max_length=20, blank=True,
                                 help_text='Format international sans le "+", ex. 2250700000000')
    telegram = models.CharField('Identifiant Telegram', max_length=50, blank=True,
                                 help_text='Sans le @, ex. azeezridwan')
    linkedin = models.URLField('URL LinkedIn', blank=True)
    github = models.URLField('URL GitHub', blank=True)
    location = models.CharField('Localisation', max_length=150, default='Abidjan, Côte d’Ivoire')
    available = models.BooleanField(
        'Disponible pour de nouveaux projets', default=True,
        help_text="Contrôle le statut affiché sur le site (pastille verte du hero et de la section À propos)."
    )

    class Meta:
        verbose_name = 'Réglages du site'
        verbose_name_plural = 'Réglages du site'

    def __str__(self):
        return 'Réglages du site'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={'email': 'contact@azeezridwan.com'})
        return obj


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('dev', 'Développement Web'),
        ('video', 'IA Créative & Vidéo'),
    ]

    name = models.CharField('Nom', max_length=100)
    category = models.CharField('Catégorie', max_length=10, choices=CATEGORY_CHOICES)
    detail = models.CharField(
        'Niveau / Usage', max_length=100,
        help_text='Ex. "Expert" pour une compétence dev, "Génération vidéo IA" pour un outil.'
    )
    order = models.PositiveIntegerField('Ordre', default=0)

    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = 'Compétence / Outil'
        verbose_name_plural = 'Compétences & Outils'

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'
