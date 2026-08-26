from django.shortcuts import get_object_or_404, render

from .models import Project

VALID_CATEGORIES = {'web', 'video'}


def project_list(request):
    """Grille filtrée. Renvoyée en partial pour les onglets HTMX,
    ou en page complète pour un accès direct à /projects/."""
    category = request.GET.get('category', 'all')
    projects = Project.objects.all()
    if category in VALID_CATEGORIES:
        projects = projects.filter(category=category)
    context = {
        'projects': projects,
        'active_category': category if category in VALID_CATEGORIES else 'all',
    }
    if request.htmx:
        return render(request, 'components/projects_grid.html', context)

    context['total_web'] = Project.objects.filter(category='web').count()
    context['total_video'] = Project.objects.filter(category='video').count()
    return render(request, 'pages/projects.html', context)


def project_detail(request, pk):
    """Détail d'un projet (problème / solution / résultat), rendu dans la modal HTMX."""
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'components/project_modal.html', {'project': project})
