from django.shortcuts import get_object_or_404, render

from .models import Project

VALID_CATEGORIES = {'web', 'video'}


def project_list(request):
    """Grille filtrée, renvoyée en partial pour les onglets HTMX."""
    category = request.GET.get('category', 'all')
    projects = Project.objects.all()
    if category in VALID_CATEGORIES:
        projects = projects.filter(category=category)
    return render(request, 'components/projects_grid.html', {
        'projects': projects,
        'active_category': category if category in VALID_CATEGORIES else 'all',
    })


def project_detail(request, pk):
    """Détail d'un projet (problème / solution / résultat), rendu dans la modal HTMX."""
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'components/project_modal.html', {'project': project})
