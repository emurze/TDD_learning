from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from apps.list.forms import CreateTodoItemForm
from apps.list.models import TodoItem


def todo_page_get(request: WSGIRequest) -> HttpResponse:
    template_name = 'list/todo.html'
    context = {
        'form': CreateTodoItemForm(),
        'items': TodoItem.objects.all(),
    }
    return render(request, template_name, context)


def todo_page_post(request: WSGIRequest) -> HttpResponse:
    TodoItem.objects.create(content=request.POST.get('content'))
    return redirect('list:todo')


@require_http_methods(['GET', 'POST'])
def todo_page_view(request: WSGIRequest) -> HttpResponse:
    match request.method:
        case 'GET':
            return todo_page_get(request)
        case 'POST':
            return todo_page_post(request)
