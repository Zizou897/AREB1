from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'order', 'created_at')
    list_filter = ('category', 'featured')
    list_editable = ('featured', 'order')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {'fields': ('title', 'category', 'sector', 'thumbnail', 'featured', 'order')}),
        ('Contenu', {'fields': ('description', 'problem', 'solution', 'result', 'stack')}),
        ('Liens', {'fields': ('live_url', 'video_url')}),
    )
