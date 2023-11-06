from unittest import TestCase

from django.db.models import QuerySet
from django.views.generic import TemplateView

from apps.list.mixins import ListItemMixin


class TestHomePageItemsListMixin(TestCase):
    """Unittest"""

    class Mixin(ListItemMixin, TemplateView):
        template_name = 'home_page.html'

    def setUp(self) -> None:
        self.view = self.Mixin()

    def test_context_data_items(self) -> None:
        context = self.view.get_context_data()
        self.assertIsInstance(context['items'], QuerySet)
