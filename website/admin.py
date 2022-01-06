from django.contrib import admin
from django.utils.safestring import mark_safe
from website import models
# Register your models here.

@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("image_view", "libele", "date_add", "status")
    date_hierarchy = "date_add" 
    list_editable = ["status"]

    def image_view(self, obj):
        return mark_safe(f'<img src="{obj.picture.url}" style="height:100px; width:150px">')
    image_view.short_description = "Aperçu des images"
    


@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("titre", "description", "date_add", "status")
    date_hierarchy = "date_add"
    list_editable = ["status"]



@admin.register(models.About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("libele", "date_add", "status")
    date_hierarchy = "date_add"
    list_editable = ["status"]




@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("titre", "icon", "date_add", "status")
    date_hierarchy = "date_add"
    list_editable = ["status"]



@admin.register(models.Technologie)
class TechnologieAdmin(admin.ModelAdmin):
    list_display = ("image_view", "nom", "date_add", "status")
    date_hierarchy = "date_add" 
    list_editable = ["status"]

    def image_view(self, obj):
        return mark_safe(f'<img src="{obj.picture.url}" style="height:100px; width:150px">')
    image_view.short_description = "Aperçu des images"


@admin.register(models.Moi_En_Avant)
class Moi_En_AvantAdmin(admin.ModelAdmin):
    list_display = ("image_view", "date_add", "status")
    date_hierarchy = "date_add" 
    list_editable = ["status"]

    def image_view(self, obj):
        return mark_safe(f'<img src="{obj.picture.url}" style="height:100px; width:150px">')
    image_view.short_description = "Aperçu des images"


@admin.register(models.Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ("image_view", "nom", "date_add", "status")
    date_hierarchy = "date_add" 
    list_editable = ["status"]

    def image_view(self, obj):
        return mark_safe(f'<img src="{obj.picture.url}" style="height:100px; width:150px">')
    image_view.short_description = "Aperçu des images"



@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "date_add", "status")
    date_hierarchy = "date_add" 
    list_editable = ["status"]



@admin.register(models.Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ("nom", "icon", "date_add", "status")
    date_hierarchy = "date_add"
    list_editable = ["status"]


@admin.register(models.Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("image_view", "email", "date_add", "status")
    date_hierarchy = "date_add" 
    list_editable = ["status"]

    def image_view(self, obj):
        return mark_safe(f'<img src="{obj.picture.url}" style="height:100px; width:150px">')
    image_view.short_description = "Aperçu des images"
