from django.contrib import admin
from django.utils.html import format_html

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('avatar_preview', 'author_name', 'author_title', 'project', 'featured', 'created_at')
    list_display_links = ('avatar_preview', 'author_name')
    list_filter = ('featured',)
    list_editable = ('featured',)
    search_fields = ('author_name', 'content')

    def avatar_preview(self, obj):
        if not obj.avatar:
            return obj.initials
        return format_html(
            '<img src="{}" style="width:36px;height:36px;object-fit:cover;border-radius:9999px;">',
            obj.avatar.url,
        )
    avatar_preview.short_description = 'Photo'
