from django.contrib import admin

from .models import SiteSettings, Skill

admin.site.site_header = 'Azeez Ridwan — Administration'
admin.site.site_title = 'Azeez Ridwan Admin'
admin.site.index_title = 'Tableau de bord'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identité', {'fields': ('name', 'location', 'available')}),
        ('Coordonnées', {'fields': ('email', 'whatsapp', 'telegram')}),
        ('Réseaux', {'fields': ('linkedin', 'github')}),
    )

    def has_add_permission(self, request):
        # Instance unique : on n'autorise l'ajout que si aucune n'existe encore.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirige directement vers la fiche unique plutôt que d'afficher une liste à un élément.
        obj = SiteSettings.load()
        from django.shortcuts import redirect
        return redirect('admin:core_sitesettings_change', obj.pk)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'detail', 'order')
    list_filter = ('category',)
    list_editable = ('detail', 'order')
    search_fields = ('name',)
    ordering = ('category', 'order', 'name')
