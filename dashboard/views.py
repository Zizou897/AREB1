from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView, View

from contact.models import ContactMessage
from core.models import SiteSettings, Skill
from projects.models import Project
from testimonials.models import Testimonial

from .forms import ProjectForm, SiteSettingsForm, SkillForm, TestimonialForm

LOGIN_URL = 'dashboard:login'


class DashboardLoginView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard:home')


class DashboardLogoutView(LogoutView):
    next_page = 'dashboard:login'


class DashboardMixin(LoginRequiredMixin):
    login_url = LOGIN_URL


# ==============================================================================
# 1. TABLEAU DE BORD
# ==============================================================================

class HomeView(DashboardMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'unread_messages': ContactMessage.objects.filter(handled=False).count(),
            'total_projects': Project.objects.count(),
            'total_testimonials': Testimonial.objects.count(),
            'total_skills': Skill.objects.count(),
            'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
            'recent_projects': Project.objects.order_by('-created_at')[:5],
        })
        return ctx


class ToggleAvailabilityView(DashboardMixin, View):
    """Toggle instantané du statut de disponibilité du studio"""
    def post(self, request):
        site_settings = SiteSettings.load()
        site_settings.available = not site_settings.available
        site_settings.save()
        status_label = 'Disponible pour de nouveaux projets' if site_settings.available else 'Actuellement en mission'
        messages.success(request, f'Disponibilité mise à jour : {status_label}.')
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('dashboard:home')
        return redirect(next_url)


# ==============================================================================
# 2. MESSAGES DE CONTACT
# ==============================================================================

class MessageListView(DashboardMixin, ListView):
    model = ContactMessage
    template_name = 'dashboard/message_list.html'
    context_object_name = 'contact_messages'
    paginate_by = 20


class MessageToggleView(DashboardMixin, View):
    def post(self, request, pk):
        message = get_object_or_404(ContactMessage, pk=pk)
        message.status = 'new' if message.handled else 'completed'
        message.save()
        return redirect('dashboard:message_list')


class MessageDeleteView(DashboardMixin, DeleteView):
    model = ContactMessage
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:message_list')

    def form_valid(self, form):
        messages.success(self.request, 'Message supprimé.')
        return super().form_valid(form)


# ==============================================================================
# 3. PROJETS PORTFOLIO
# ==============================================================================

class ProjectListView(DashboardMixin, ListView):
    model = Project
    template_name = 'dashboard/project_list.html'
    context_object_name = 'projects'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_count'] = Project.objects.count()
        ctx['web_count'] = Project.objects.filter(category='web').count()
        ctx['video_count'] = Project.objects.filter(category='video').count()
        ctx['featured_count'] = Project.objects.filter(featured=True).count()
        return ctx


class ProjectCreateView(DashboardMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/project_form.html'
    success_url = reverse_lazy('dashboard:project_list')

    def form_valid(self, form):
        last_order = Project.objects.aggregate(Max('order'))['order__max']
        form.instance.order = (last_order or 0) + 1
        messages.success(self.request, f'Projet « {form.instance.title} » créé.')
        return super().form_valid(form)


class ProjectUpdateView(DashboardMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/project_form.html'
    success_url = reverse_lazy('dashboard:project_list')

    def form_valid(self, form):
        messages.success(self.request, f'Projet « {form.instance.title} » mis à jour.')
        return super().form_valid(form)


class ProjectDeleteView(DashboardMixin, DeleteView):
    model = Project
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:project_list')

    def form_valid(self, form):
        messages.success(self.request, f'Projet « {self.object.title} » supprimé.')
        return super().form_valid(form)


class ProjectToggleFeaturedView(DashboardMixin, View):
    """Toggle en 1 clic pour mettre un projet en avant sur la page d'accueil"""
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.featured = not project.featured
        project.save(update_fields=['featured'])
        state = 'mis en avant' if project.featured else 'retiré de la mise en avant'
        messages.success(request, f'Projet « {project.title} » {state}.')
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('dashboard:project_list')
        return redirect(next_url)


# ==============================================================================
# 4. TÉMOIGNAGES & AVIS
# ==============================================================================

class TestimonialListView(DashboardMixin, ListView):
    model = Testimonial
    template_name = 'dashboard/testimonial_list.html'
    context_object_name = 'testimonials'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_count'] = Testimonial.objects.count()
        ctx['featured_count'] = Testimonial.objects.filter(featured=True).count()
        return ctx


class TestimonialCreateView(DashboardMixin, CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'dashboard/testimonial_form.html'
    success_url = reverse_lazy('dashboard:testimonial_list')

    def form_valid(self, form):
        messages.success(self.request, 'Témoignage ajouté.')
        return super().form_valid(form)


class TestimonialUpdateView(DashboardMixin, UpdateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'dashboard/testimonial_form.html'
    success_url = reverse_lazy('dashboard:testimonial_list')

    def form_valid(self, form):
        messages.success(self.request, 'Témoignage mis à jour.')
        return super().form_valid(form)


class TestimonialDeleteView(DashboardMixin, DeleteView):
    model = Testimonial
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:testimonial_list')

    def form_valid(self, form):
        messages.success(self.request, 'Témoignage supprimé.')
        return super().form_valid(form)


class TestimonialToggleFeaturedView(DashboardMixin, View):
    def post(self, request, pk):
        t = get_object_or_404(Testimonial, pk=pk)
        t.featured = not t.featured
        t.save(update_fields=['featured'])
        state = 'mis en avant' if t.featured else 'retiré de la mise en avant'
        messages.success(request, f'Témoignage de {t.author_name} {state}.')
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('dashboard:testimonial_list')
        return redirect(next_url)


# ==============================================================================
# 5. COMPÉTENCES & OUTILS
# ==============================================================================

class SkillListView(DashboardMixin, ListView):
    model = Skill
    template_name = 'dashboard/skill_list.html'
    context_object_name = 'skills'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dev_skills'] = Skill.objects.filter(category='dev')
        ctx['video_skills'] = Skill.objects.filter(category='video')
        return ctx


class SkillCreateView(DashboardMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'dashboard/skill_form.html'
    success_url = reverse_lazy('dashboard:skill_list')

    def form_valid(self, form):
        messages.success(self.request, f'Compétence « {form.instance.name} » ajoutée.')
        return super().form_valid(form)


class SkillUpdateView(DashboardMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'dashboard/skill_form.html'
    success_url = reverse_lazy('dashboard:skill_list')

    def form_valid(self, form):
        messages.success(self.request, f'Compétence « {form.instance.name} » mise à jour.')
        return super().form_valid(form)


class SkillDeleteView(DashboardMixin, DeleteView):
    model = Skill
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:skill_list')

    def form_valid(self, form):
        messages.success(self.request, f'Compétence « {self.object.name} » supprimée.')
        return super().form_valid(form)


# ==============================================================================
# 6. RÉGLAGES DU SITE & STUDIO
# ==============================================================================

class SiteSettingsUpdateView(DashboardMixin, UpdateView):
    model = SiteSettings
    form_class = SiteSettingsForm
    template_name = 'dashboard/settings_form.html'
    success_url = reverse_lazy('dashboard:settings')

    def get_object(self, queryset=None):
        return SiteSettings.load()

    def form_valid(self, form):
        messages.success(self.request, 'Réglages du site mis à jour.')
        return super().form_valid(form)
