from django.db import models


class ContactMessage(models.Model):
    full_name = models.CharField('Prénom & Nom', max_length=150)
    email = models.EmailField('Email')
    message = models.TextField('Message')
    created_at = models.DateTimeField('Reçu le', auto_now_add=True)
    handled = models.BooleanField('Traité', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'

    def __str__(self):
        return f'{self.full_name} ({self.created_at:%d/%m/%Y})'
