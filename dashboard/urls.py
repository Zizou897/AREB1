from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.DashboardLoginView.as_view(), name='login'),
    path('logout/', views.DashboardLogoutView.as_view(), name='logout'),
    path('', views.HomeView.as_view(), name='home'),
    path('disponibilite/basculer/', views.ToggleAvailabilityView.as_view(), name='toggle_availability'),

    # Messages de contact
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/basculer/', views.MessageToggleView.as_view(), name='message_toggle'),
    path('messages/<int:pk>/supprimer/', views.MessageDeleteView.as_view(), name='message_delete'),

    # Projets
    path('projets/', views.ProjectListView.as_view(), name='project_list'),
    path('projets/nouveau/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projets/<int:pk>/modifier/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projets/<int:pk>/supprimer/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('projets/<int:pk>/toggle-star/', views.ProjectToggleFeaturedView.as_view(), name='project_toggle_featured'),

    # Témoignages
    path('temoignages/', views.TestimonialListView.as_view(), name='testimonial_list'),
    path('temoignages/nouveau/', views.TestimonialCreateView.as_view(), name='testimonial_create'),
    path('temoignages/<int:pk>/modifier/', views.TestimonialUpdateView.as_view(), name='testimonial_update'),
    path('temoignages/<int:pk>/supprimer/', views.TestimonialDeleteView.as_view(), name='testimonial_delete'),
    path('temoignages/<int:pk>/toggle-star/', views.TestimonialToggleFeaturedView.as_view(), name='testimonial_toggle_featured'),

    # Compétences
    path('competences/', views.SkillListView.as_view(), name='skill_list'),
    path('competences/nouveau/', views.SkillCreateView.as_view(), name='skill_create'),
    path('competences/<int:pk>/modifier/', views.SkillUpdateView.as_view(), name='skill_update'),
    path('competences/<int:pk>/supprimer/', views.SkillDeleteView.as_view(), name='skill_delete'),

    # Réglages
    path('reglages/', views.SiteSettingsUpdateView.as_view(), name='settings'),
]
