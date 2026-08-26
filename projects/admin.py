from django.contrib import admin
from django.utils.html import format_html

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title', 'category', 'sector', 'featured', 'order', 'created_at')
    list_display_links = ('thumbnail_preview', 'title')
    list_filter = ('category', 'featured')
    list_editable = ('featured', 'order')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {'fields': ('title', 'category', 'sector', 'thumbnail', 'featured', 'order')}),
        ('Contenu', {'fields': ('description', 'problem', 'solution', 'result', 'stack')}),
        ('Liens', {'fields': ('live_url', 'video_url')}),
    )

    def thumbnail_preview(self, obj):
        if not obj.thumbnail:
            return '—'
        return format_html(
            '<img src="{}" style="width:64px;height:40px;object-fit:cover;border-radius:4px;">',
            obj.thumbnail.url,
        )
    thumbnail_preview.short_description = 'Aperçu'
