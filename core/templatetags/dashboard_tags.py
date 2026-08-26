from django import template

from contact.models import ContactMessage
from projects.models import Project
from testimonials.models import Testimonial

register = template.Library()


@register.inclusion_tag('admin/_dashboard_stats.html')
def dashboard_stats():
    return {
        'unread_messages': ContactMessage.objects.filter(handled=False).count(),
        'total_projects': Project.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
        'recent_messages': ContactMessage.objects.filter(handled=False).order_by('-created_at')[:5],
        'recent_projects': Project.objects.order_by('-created_at')[:5],
    }
