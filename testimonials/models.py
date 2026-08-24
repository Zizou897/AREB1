from django.db import models


class Testimonial(models.Model):
    author_name = models.CharField('Nom', max_length=100)
    author_title = models.CharField('Poste / Entreprise', max_length=150)
    content = models.TextField('Témoignage')
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL,
                                null=True, blank=True, verbose_name='Projet lié')
    avatar = models.ImageField('Photo', upload_to='testimonials/', blank=True)
    featured = models.BooleanField('Mis en avant', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-featured', '-created_at']
        verbose_name = 'Témoignage'

    def __str__(self):
        return f'{self.author_name} — {self.author_title}'

    @property
    def initials(self):
        parts = self.author_name.split()
        return ''.join(p[0].upper() for p in parts[:2]) or '•'
