from django.core.cache import cache


def client_ip(request):
    """IP réelle du visiteur derrière le reverse proxy Nginx (X-Real-IP)."""
    forwarded = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def is_rate_limited(key_prefix, ip, limits):
    """Incrémente les compteurs et renvoie True si l'une des limites est dépassée.

    `limits` : itérable de (label, limit, window_seconds).
    """
    limited = False
    for label, limit, window in limits:
        key = f'{key_prefix}_{label}_{ip}'
        count = cache.get(key)
        if count is None:
            cache.set(key, 1, timeout=window)
        elif count >= limit:
            limited = True
        else:
            cache.incr(key)
    return limited
