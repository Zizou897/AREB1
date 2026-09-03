from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('set-language/<str:lang_code>/', views.set_language, name='set_language'),
    path('mentions-legales/', views.legal, name='legal'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]

