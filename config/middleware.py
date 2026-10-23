from django.conf import settings

FRONTEND_VERSION_COOKIE = 'frontend_version'
FRONTEND_VERSION_COOKIE_AGE = 60 * 60 * 24 * 365


class FrontendVersionMiddleware:
    """
    Сбрасывает кэш браузера, когда меняется FRONTEND_VERSION.

    - HTML-страницы отдаются с Cache-Control: no-cache, чтобы браузер
      всегда сверял их с сервером и получал свежие ссылки на статику.
    - Если версия в cookie пользователя отличается от текущей, отправляется
      Clear-Site-Data: "cache" (один раз), и cookie обновляется.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not response.get('Content-Type', '').startswith('text/html'):
            return response

        if not response.has_header('Cache-Control'):
            response['Cache-Control'] = 'no-cache'

        version = settings.FRONTEND_VERSION
        if version and request.COOKIES.get(FRONTEND_VERSION_COOKIE) != version:
            response['Clear-Site-Data'] = '"cache"'
            response.set_cookie(
                FRONTEND_VERSION_COOKIE,
                version,
                max_age=FRONTEND_VERSION_COOKIE_AGE,
                secure=True,
                httponly=True,
                samesite='Lax',
            )

        return response
