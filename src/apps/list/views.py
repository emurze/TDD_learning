import logging

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from apps.list.forms import TodoCreateItemForm
from apps.list.models import List, ListItem

lg = logging.getLogger(__name__)


class HomePageView(CreateView):
    template_name = 'list/home_page.html'
    form_class = TodoCreateItemForm

    def get_context_data(self, **kwargs) -> dict:
        kwargs['todo_form'] = {
            'label': 'Create To-Do list',
            'action': '/',
        }
        return super().get_context_data(**kwargs)

    def form_valid(self, form: TodoCreateItemForm) -> HttpResponse:
        user_id = self.request.user.id

        new_list = List.objects.get_or_create(slug=f'{user_id}_list')[0]

        form = form.save(commit=False)
        form.list = new_list
        form.save()
        return redirect(new_list.get_absolute_url())


def my_list_view(request: WSGIRequest, slug: str) -> HttpResponse:
    extra_context = {}

    if request.method == 'POST':
        if (form := TodoCreateItemForm(request.POST)).is_valid():
            form = form.save(commit=False)

            new_list = List.objects.get_or_create(slug=slug)[0]

            form.list = new_list
            form.save()
            return redirect(new_list.get_absolute_url())
        else:
            extra_context['form'] = form

    items = ListItem.objects.filter(list__slug=slug)
    context = {
        'items': items,
        'form': TodoCreateItemForm(),
        'todo_form': {
            'label': 'Your To-Do list',
            'action': List(slug=slug).get_absolute_url(),
        },
    } | extra_context
    return render(request, 'list/list.html', context)
