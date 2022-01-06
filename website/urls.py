from django.urls import path
from website import views



urlpatterns = [
    path('', views.index, name="index"),
    path('projet/<int:id>', views.project, name="project"),
    path('terms/', views.terms, name="terms"),
    path('privacy/', views.privacy, name="privacy"),
    path('download/', views.downloadFile, name="cv")
    
]
