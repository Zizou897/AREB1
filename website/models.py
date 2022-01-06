from django.db import models

from autoslug import AutoSlugField
from tinymce.models import HTMLField
# Create your models here.

class Base(models.Model):
    date_add = models.DateField(auto_now_add=True)
    date_update = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True
    

class Banner(Base):
    libele = models.CharField(max_length=250)
    picture = models.FileField(upload_to="image_banner")

    class Meta:
        verbose_name = "Bannière"
        verbose_name_plural = "Bannières"
    
    def __str__(self):
        return self.libele
    




class Experience(Base):
    titre = models.CharField( max_length=50)
    description = HTMLField()
    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
    
    def __str__(self):
        return self.titre



class About(Base):
    libele = models.CharField(max_length=250)
    description = models.TextField()
    experience = models.ManyToManyField("website.Experience",related_name="about_experience")

    class Meta:
        verbose_name = "A propos"
        verbose_name_plural = "A propos"
    
    def __str__(self):
        return self.libele


    

class Service(Base):
    icon = models.CharField( max_length=50)
    titre = models.CharField( max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.titre
    


class Technologie(Base):
    nom = models.CharField(max_length=50)
    picture = models.FileField(upload_to="image_techno")

    class Meta:
        verbose_name = "Technologie"
        verbose_name_plural = "Technologies"
    
    def __str__(self):
        return self.nom


class Moi_En_Avant(Base):
    texte = models.CharField(max_length=50)
    picture = models.FileField(upload_to="image_moi")
    description = HTMLField()
    technologie = models.ManyToManyField("website.Technologie", related_name="techno")

    class Meta:
        verbose_name = "Moi_En_Avant"
        verbose_name_plural = "Moi_En_Avant"
    
    def __str__(self):
        return self.texte




class Projet(Base):
    nom = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    slug = AutoSlugField(populate_from="nom", null=True)
    picture = models.FileField(upload_to="image_projet")
    picture2 = models.FileField(upload_to="image_projet")
    description = HTMLField()
    description2 = HTMLField()

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
    
    def __str__(self):
        return self.nom

class Contact(Base):
    nom = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    message = models.TextField()

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
    
    def __str__(self):
        return self.nom

class Social(Base):
    nom = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    url = models.URLField(max_length=200)

    class Meta:
        verbose_name = "Social"
        verbose_name_plural = "Sociaux"
    
    def __str__(self):
        return self.nom


class Website(Base):
    nom = models.CharField(max_length=50)
    picture = models.FileField(upload_to="image_web")
    email = models.EmailField(max_length=254)
    description_service = models.TextField()
    description_project = models.TextField()
    description_conctact = models.TextField()

    class Meta:
        verbose_name = "Website"
        verbose_name_plural = "Websites"
    
    def __str__(self):
        return self.nom
