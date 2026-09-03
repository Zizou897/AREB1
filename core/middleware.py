from urllib.parse import urlsplit

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    """Redirige le sous-domaine www vers le domaine apex (évite le contenu dupliqué)."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.canonical_host = urlsplit(settings.SITE_URL).netloc

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        if host == f'www.{self.canonical_host}':
            target = f'{request.scheme}://{self.canonical_host}{request.get_full_path()}'
            return HttpResponsePermanentRedirect(target)
        return self.get_response(request)
