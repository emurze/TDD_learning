from django.core.handlers.wsgi import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def home_page_view(request: HttpRequest) -> HttpResponse:
    template_name = 'list/home_page.html'
    return render(request, template_name)
