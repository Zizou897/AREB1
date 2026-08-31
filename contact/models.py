import re
from django.db import models


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('contacted', 'Contacté'),
        ('proposal', 'Proposition envoyée'),
        ('won', 'Projet Gagné'),
        ('completed', 'Livré / Terminé'),
        ('lost', 'Archivé / Sans suite'),
    ]

    SERVICE_CHOICES = [
        ('web', 'Développement Web'),
        ('video', 'Vidéo IA'),
        ('combo', 'Pack Dev + Vidéo'),
        ('consulting', 'Consulting & Audit'),
        ('other', 'Autre besoin'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    ]

    full_name = models.CharField('Prénom & Nom', max_length=150)
    email = models.EmailField('Email')
    phone = models.CharField('Téléphone / WhatsApp', max_length=50, blank=True)
    company = models.CharField('Entreprise / Organisation', max_length=150, blank=True)
    message = models.TextField('Message')

    status = models.CharField('Statut CRM', max_length=20, choices=STATUS_CHOICES, default='new')
    service_type = models.CharField('Type de prestation', max_length=20, choices=SERVICE_CHOICES, default='web')
    priority = models.CharField('Priorité', max_length=10, choices=PRIORITY_CHOICES, default='medium')
    budget = models.DecimalField('Budget estimé (FCFA)', max_digits=12, decimal_places=0, null=True, blank=True)
    notes = models.TextField('Notes internes / Suivi', blank=True)
    last_contact_date = models.DateTimeField('Dernier contact', null=True, blank=True)

    created_at = models.DateTimeField('Reçu le', auto_now_add=True)
    handled = models.BooleanField('Traité', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prospect / Message'
        verbose_name_plural = 'Prospects / Messages'

    def __str__(self):
        comp = f' ({self.company})' if self.company else ''
        return f'{self.full_name}{comp} — {self.get_status_display()}'

    def save(self, *args, **kwargs):
        # Sync handled boolean with status
        if self.status in ['won', 'completed', 'lost']:
            self.handled = True
        elif self.status == 'new':
            self.handled = False
        super().save(*args, **kwargs)

    @property
    def whatsapp_number(self):
        """Nettoie le numéro pour un lien direct wa.me"""
        if not self.phone:
            return ''
        digits = re.sub(r'\D', '', self.phone)
        return digits

    @property
    def budget_display(self):
        """Formatte le montant avec séparateur de milliers"""
        if self.budget is None:
            return 'Non précisé'
        return f'{int(self.budget):,} FCFA'.replace(',', ' ')


class LeadActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('note', 'Note interne'),
        ('call', 'Appel téléphonique'),
        ('whatsapp', 'Échange WhatsApp'),
        ('email', 'Email envoyé'),
        ('meeting', 'Rendez-vous / Visio'),
        ('status_change', 'Changement d’étape'),
    ]

    lead = models.ForeignKey(
        ContactMessage,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name='Prospect'
    )
    activity_type = models.CharField('Type d’action', max_length=20, choices=ACTIVITY_TYPE_CHOICES, default='note')
    content = models.TextField('Détails / Compte-rendu')
    created_at = models.DateTimeField('Date', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Activité prospect'
        verbose_name_plural = 'Activités prospects'

    def __str__(self):
        return f'{self.get_activity_type_display()} - {self.lead.full_name} ({self.created_at:%d/%m/%Y})'
