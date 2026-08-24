from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'created_at', 'handled')
    list_filter = ('handled',)
    list_editable = ('handled',)
    search_fields = ('full_name', 'email', 'message')
    readonly_fields = ('full_name', 'email', 'message', 'created_at')

    def has_add_permission(self, request):
        return False
