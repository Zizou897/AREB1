from django.contrib import admin
from .models import ContactMessage, LeadActivity


class LeadActivityInline(admin.TabularInline):
    model = LeadActivity
    extra = 1
    fields = ('activity_type', 'content', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company', 'email', 'phone', 'service_type', 'status', 'priority', 'budget', 'created_at')
    list_filter = ('status', 'service_type', 'priority', 'handled', 'created_at')
    list_editable = ('status', 'priority')
    search_fields = ('full_name', 'email', 'company', 'message', 'phone')
    inlines = [LeadActivityInline]


@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    list_display = ('lead', 'activity_type', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('lead__full_name', 'content')
