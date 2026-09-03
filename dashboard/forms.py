import logging
import os
import tempfile
from pathlib import Path

from django import forms
from django.core.files import File
from django.core.files.uploadedfile import UploadedFile

from core.models import SiteSettings, Skill
from projects.media_processing import MAX_VIDEO_SIZE, compress_video, extract_thumbnail
from projects.models import Project
from testimonials.models import Testimonial

logger = logging.getLogger(__name__)

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
            'live_url', 'video_file',
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
            'video_file': forms.ClearableFileInput(attrs={'class': INPUT + ' py-2.5', 'accept': 'video/mp4,video/webm,video/quicktime'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['stack'].initial = ', '.join(self.instance.stack or [])
        else:
            self.fields['category'].initial = 'web'
        # La miniature peut être générée automatiquement depuis la vidéo (voir clean_thumbnail).
        self.fields['thumbnail'].required = False

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if not thumbnail and self.cleaned_data.get('category') != 'video':
            raise forms.ValidationError('Ce champ est obligatoire pour un projet web.')
        return thumbnail

    def save(self, commit=True):
        instance = super().save(commit=False)
        raw = self.cleaned_data.get('stack', '')
        instance.stack = [item.strip() for item in raw.split(',') if item.strip()]

        video = self.cleaned_data.get('video_file')
        if video and 'video_file' in self.changed_data and isinstance(video, UploadedFile):
            self._process_video(instance, video)

        if commit:
            instance.save()
        return instance

    def _process_video(self, instance, uploaded_video):
        """Compresse la vidéo si >20 Mo et génère une miniature si aucune n'a été fournie."""
        suffix = Path(uploaded_video.name).suffix or '.mp4'
        stem = Path(uploaded_video.name).stem or 'video'

        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = os.path.join(tmpdir, f'src{suffix}')
            with open(src_path, 'wb') as f:
                for chunk in uploaded_video.chunks():
                    f.write(chunk)

            final_video_path = src_path
            if uploaded_video.size > MAX_VIDEO_SIZE:
                compressed_path = os.path.join(tmpdir, 'compressed.mp4')
                try:
                    compress_video(src_path, compressed_path)
                    final_video_path = compressed_path
                except Exception:
                    logger.exception('Échec de la compression vidéo pour %s', uploaded_video.name)

            with open(final_video_path, 'rb') as f:
                instance.video_file.save(f'{stem}.mp4', File(f), save=False)

            if not self.cleaned_data.get('thumbnail'):
                thumb_path = os.path.join(tmpdir, 'thumb.jpg')
                try:
                    extract_thumbnail(final_video_path, thumb_path)
                    with open(thumb_path, 'rb') as f:
                        instance.thumbnail.save(f'{stem}_thumb.jpg', File(f), save=False)
                except Exception:
                    logger.exception('Échec de la génération de miniature pour %s', uploaded_video.name)


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
        fields = [
            'name', 'email', 'whatsapp', 'telegram', 'linkedin', 'github', 'location', 'available',
            'showcase_video_1', 'showcase_video_2',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT}),
            'email': forms.EmailInput(attrs={'class': INPUT}),
            'whatsapp': forms.TextInput(attrs={'class': INPUT, 'placeholder': '2250700000000'}),
            'telegram': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'azeezridwan'}),
            'linkedin': forms.URLInput(attrs={'class': INPUT, 'placeholder': 'https://linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'class': INPUT, 'placeholder': 'https://github.com/...'}),
            'location': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Abidjan, Côte d’Ivoire'}),
            'available': forms.CheckboxInput(attrs={'class': CHECKBOX}),
            'showcase_video_1': forms.Select(attrs={'class': INPUT}),
            'showcase_video_2': forms.Select(attrs={'class': INPUT}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        video_qs = Project.objects.filter(category='video').order_by('-created_at')
        self.fields['showcase_video_1'].queryset = video_qs
        self.fields['showcase_video_2'].queryset = video_qs
        self.fields['showcase_video_1'].empty_label = 'Aucune'
        self.fields['showcase_video_2'].empty_label = 'Aucune'
