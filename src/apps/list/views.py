import logging

from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import CreateView

from apps.list.domain import JsonStatus
from apps.list.forms import TodoCreateItemForm, TodoEmailForm
from apps.list.models import List, ListItem

lg = logging.getLogger(__name__)


class HomePageView(CreateView):
    template_name = 'list/home_page.html'
    form_class = TodoCreateItemForm
    extra_context = {
        'todo_form': {
            'label': 'Create To-Do list',
            'action': '/',
        },
        'email_form': TodoEmailForm(),
        'email_form_action': reverse_lazy('send_email'),
    }

    def form_valid(self, form: TodoCreateItemForm) -> HttpResponse:
        user_id = self.request.user.id

        new_list = List.objects.get_or_create(slug=f'{user_id}_list')[0]

        form = form.save(commit=False)
        form.list = new_list
        form.save()
        return redirect(new_list.get_absolute_url())


@require_http_methods(["GET", "POST"])
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


@require_POST
def send_email(request: WSGIRequest) -> HttpResponse:
    if (form := TodoEmailForm(data=request.POST)).is_valid():
        cd = form.cleaned_data
        send_mail(
            'Your login link for SuperLists',
            'body text tbc',
            'noreply@superlists',
            [cd['email']],
        )
        return JsonResponse({'status': JsonStatus.OK})
    else:
        return JsonResponse({'status': JsonStatus.ERROR})
