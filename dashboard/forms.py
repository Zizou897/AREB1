from django import forms

from core.models import SiteSettings, Skill
from projects.models import Project
from testimonials.models import Testimonial

INPUT = (
    'w-full rounded-xl border border-line bg-surface-2 px-4 py-3 text-ink '
    'placeholder:text-ink-mute/70 focus:border-cyan focus:outline-none '
    'focus:ring-2 focus:ring-cyan/30 transition-colors min-h-[46px]'
)
CHECKBOX = 'h-5 w-5 rounded border-line bg-surface-2 text-cyan focus:ring-cyan/30 cursor-pointer accent-cyan'


class ProjectForm(forms.ModelForm):
    stack = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Django, HTMX, TailwindCSS, PostgreSQL'}),
        help_text='Technologies séparées par une virgule.',
    )

    class Meta:
        model = Project
        fields = [
            'title', 'category', 'sector', 'thumbnail', 'featured',
            'description', 'problem', 'solution', 'result',
            'live_url', 'video_url',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Ex: Portail E-commerce Artisanal'}),
            'category': forms.Select(attrs={'class': INPUT}),
            'sector': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'E-commerce, Restauration, Fintech…'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': INPUT + ' py-2.5'}),
            'featured': forms.CheckboxInput(attrs={'class': CHECKBOX}),
            'description': forms.Textarea(attrs={'class': INPUT, 'rows': 3, 'placeholder': 'Description générale du projet'}),
            'problem': forms.Textarea(attrs={'class': INPUT, 'rows': 3, 'placeholder': 'Quel problème précis le client rencontrait-il ?'}),
            'solution': forms.Textarea(attrs={'class': INPUT, 'rows': 3, 'placeholder': 'Quelle architecture et solution technique ont été déployées ?'}),
            'result': forms.Textarea(attrs={'class': INPUT, 'rows': 3, 'placeholder': 'Résultat chiffré (ex. +45% de conversion, temps de chargement divisé par 3)'}),
            'live_url': forms.URLInput(attrs={'class': INPUT, 'placeholder': 'https://monsite.com'}),
            'video_url': forms.URLInput(attrs={'class': INPUT, 'placeholder': 'https://youtube.com/watch?v=... ou https://vimeo.com/...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['stack'].initial = ', '.join(self.instance.stack or [])
        else:
            self.fields['category'].initial = 'web'

    def save(self, commit=True):
        instance = super().save(commit=False)
        raw = self.cleaned_data.get('stack', '')
        instance.stack = [item.strip() for item in raw.split(',') if item.strip()]
        if commit:
            instance.save()
        return instance


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['author_name', 'author_title', 'content', 'project', 'avatar', 'featured']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Amadou Diallo'}),
            'author_title': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'CEO, Ivoire Digital Group'}),
            'content': forms.Textarea(attrs={'class': INPUT, 'rows': 4, 'placeholder': 'Témoignage du client...'}),
            'project': forms.Select(attrs={'class': INPUT}),
            'avatar': forms.ClearableFileInput(attrs={'class': INPUT + ' py-2.5'}),
            'featured': forms.CheckboxInput(attrs={'class': CHECKBOX}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'detail', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Ex: Python / Django ou Runway Gen-3'}),
            'category': forms.Select(attrs={'class': INPUT}),
            'detail': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Expert, Architecture API, Production 4K…'}),
            'order': forms.NumberInput(attrs={'class': INPUT}),
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['name', 'email', 'whatsapp', 'telegram', 'linkedin', 'github', 'location', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT}),
            'email': forms.EmailInput(attrs={'class': INPUT}),
            'whatsapp': forms.TextInput(attrs={'class': INPUT, 'placeholder': '2250700000000'}),
            'telegram': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'azeezridwan'}),
            'linkedin': forms.URLInput(attrs={'class': INPUT, 'placeholder': 'https://linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'class': INPUT, 'placeholder': 'https://github.com/...'}),
            'location': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Abidjan, Côte d’Ivoire'}),
            'available': forms.CheckboxInput(attrs={'class': CHECKBOX}),
        }
