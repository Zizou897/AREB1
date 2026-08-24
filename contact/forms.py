from django import forms

from .models import ContactMessage

BASE_INPUT = (
    'w-full rounded-xl border border-line bg-surface-2 px-4 py-3 text-ink '
    'placeholder:text-ink-mute/70 focus:border-cyan focus:outline-none '
    'focus:ring-2 focus:ring-cyan/30 transition-colors min-h-[48px]'
)


class ContactForm(forms.ModelForm):
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
