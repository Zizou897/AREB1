from django import forms

from .models import ContactMessage

BASE_INPUT = (
    'w-full rounded-xl border border-line bg-surface-2 px-4 py-3 text-ink '
    'placeholder:text-ink-mute/70 focus:border-cyan focus:outline-none '
    'focus:ring-2 focus:ring-cyan/30 transition-colors min-h-[48px]'
)


class ContactForm(forms.ModelForm):
    # Honeypot anti-spam : champ texte réel (donc rempli par les bots qui remplissent
    # tout formulaire), mais masqué hors écran en CSS pour rester invisible à un humain.
    # Ne correspond à aucun champ du modèle — jamais sauvegardé.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}),
    )

    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': BASE_INPUT, 'placeholder': 'Awa Koné',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': BASE_INPUT, 'placeholder': 'vous@exemple.com',
                'autocomplete': 'email',
            }),
            'message': forms.Textarea(attrs={
                'class': BASE_INPUT + ' resize-y', 'rows': 6,
                'placeholder': 'Une question, un projet, une opportunité… je vous lis.',
            }),
        }
