import os
import mimetypes
from pathlib import Path
from django.http.response import HttpResponse
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404

from website import models


def index(request): 
    banner = models.Banner.objects.filter(status=True).first()
    services = models.Service.objects.filter(status=True)
    experiences = models.Experience.objects.filter(status=True)
    moiEnAvant = models.Moi_En_Avant.objects.filter(status=True).first()
    projects = models.Projet.objects.filter(status=True)
    sociaux = models.Social.objects.filter(status=True)
    sociau = models.Social.objects.filter(status=True)[:2]
    site = models.Website.objects.filter(status=True).first()
    technologies = models.Technologie.objects.filter(status=True)
    return render(request, "index.html", locals())


def project(request, id=None):
    sociaux = models.Social.objects.filter(status=True)
    sociau = models.Social.objects.filter(status=True)[:2]
    site = models.Website.objects.filter(status=True).first()
    projectId = get_object_or_404(models.Projet, id=id)
    return render(request, "project.html", locals()) 


def privacy(request):
    return render(request, "privacy.html", locals()) 


def terms(request):
    return render(request, "terms.html", locals()) 


def downloadFile(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fileName = 'cv.pdf'
    filePath = BASE_DIR + '/static/file/' + fileName
    path = open(filePath, "rb")
    mime_type, _ = mimetypes.guess_type(filePath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % fileName
    return response