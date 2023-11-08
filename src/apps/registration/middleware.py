from collections.abc import Callable

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.open_urls = [self.login_url] + getattr(settings, 'OPEN_URLS', [])

    def __call__(self, request: WSGIRequest):
        user = request.user
        url = request.path_info

        if not user.is_authenticated and url not in self.open_urls:

            if request.path == settings.LOGIN_URL:
                path = ''
            else:
                path = request.path

            return redirect(self.login_url + f'?next={path}')

        return self.get_response(request)
