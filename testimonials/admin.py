from django.contrib import admin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title', 'project', 'featured', 'created_at')
    list_filter = ('featured',)
    list_editable = ('featured',)
    search_fields = ('author_name', 'content')
