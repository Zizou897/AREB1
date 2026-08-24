from django.db import models

AI_TOOLS = [
    'Runway ML', 'Kling AI', 'ElevenLabs', 'Sora',
    'Pika Labs', 'Adobe Firefly', 'CapCut AI',
]


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Développement web'),
        ('video', 'Vidéo IA publicitaire'),
    ]

    title = models.CharField('Titre', max_length=200)
    category = models.CharField('Catégorie', max_length=10, choices=CATEGORY_CHOICES)
    sector = models.CharField('Secteur', max_length=100, blank=True,
                              help_text='Pour les vidéos IA : e-commerce, restauration, immobilier…')
    description = models.TextField('Description')
    problem = models.TextField('Problème client résolu', blank=True)
    solution = models.TextField('Solution apportée', blank=True)
    result = models.TextField('Résultat mesurable', blank=True)
    stack = models.JSONField('Stack / Outils', default=list,
                             help_text='Liste JSON, ex. ["Django", "PostgreSQL"]')
    live_url = models.URLField('URL du site', blank=True)
    video_url = models.URLField('URL de la vidéo', blank=True,
                                help_text='Lien YouTube ou Vimeo pour les vidéos IA')
    thumbnail = models.ImageField('Miniature', upload_to='projects/')
    featured = models.BooleanField('Mis en avant', default=False)
    order = models.PositiveIntegerField('Ordre', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Projet'

    def __str__(self):
        return self.title

    @property
    def video_embed_url(self):
        """Convertit une URL YouTube/Vimeo en URL d'embed pour l'iframe de la modal."""
        url = self.video_url
        if not url:
            return ''
        if 'youtube.com/watch' in url:
            video_id = url.split('v=')[-1].split('&')[0]
            return f'https://www.youtube-nocookie.com/embed/{video_id}?autoplay=1&rel=0'
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
            return f'https://www.youtube-nocookie.com/embed/{video_id}?autoplay=1&rel=0'
        if 'vimeo.com/' in url and '/video/' not in url:
            video_id = url.rstrip('/').split('/')[-1]
            return f'https://player.vimeo.com/video/{video_id}?autoplay=1'
        return url
