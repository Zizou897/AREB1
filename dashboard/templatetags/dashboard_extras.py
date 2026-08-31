from django import template

from contact.models import ContactMessage

register = template.Library()


@register.simple_tag
def unread_message_count():
    return ContactMessage.objects.filter(handled=False).count()
