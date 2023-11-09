import logging

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView

from apps.list.forms import TodoCreateItemForm
from apps.list.models import List, ListItem

lg = logging.getLogger(__name__)


class HomePageView(CreateView):
    template_name = 'list/home_page.html'
    form_class = TodoCreateItemForm

    def get_context_data(self, **kwargs) -> dict:
        kwargs['todo_form'] = {
            'label': 'Create to-do list',
            'action': '/',
        }
        return super().get_context_data(**kwargs)

    def get_success_url(self) -> str:
        return reverse('lists', args=(f'{self.request.user.id}_list', ))

    def form_valid(self, form: TodoCreateItemForm) -> HttpResponse:
        user_id = self.request.user.id

        try:
            new_list = List.objects.get(slug=f'{user_id}_list')
        except List.DoesNotExist:
            new_list = List.objects.create(slug=f'{user_id}_list')

        form = form.save(commit=False)
        form.list = new_list
        form.save()
        return redirect(self.get_success_url())


def my_list_view(request: WSGIRequest, slug: str) -> HttpResponse:
    if (form := TodoCreateItemForm(request.POST)).is_valid():
        form = form.save(commit=False)

        try:
            new_list = List.objects.get(slug=slug)
        except List.DoesNotExist:
            new_list = List.objects.create(slug=slug)

        form.list = new_list
        form.save()
        return redirect(reverse('lists', args=(f'{request.user.id}_list', )))
    else:
        items = ListItem.objects.filter(list__slug=slug)
        form = TodoCreateItemForm()

    context = {
        'items': items,
        'form': form,
        'todo_form': {
            'label': 'Your to-do list',
            'action': reverse('lists', args=(f'{request.user.id}_list', )),
        },
    }
    return render(request, 'list/list.html', context)
