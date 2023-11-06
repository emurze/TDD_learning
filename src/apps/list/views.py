from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.list.forms import TodoCreateItemForm
from apps.list.mixins import ListItemMixin


class HomePageView(ListItemMixin, CreateView):
    template_name = 'home_page.html'
    form_class = TodoCreateItemForm
    success_url = reverse_lazy('home_page')
