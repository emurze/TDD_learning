from django.db.models import QuerySet
from django.test import TestCase

from django.views.generic import TemplateView

from apps.list.mixins import ListItemsMixin


class TestListItemsMixinTest(TestCase):
    class View(ListItemsMixin, TemplateView):
        pass

    def setUp(self):
        self.view = self.View()

    def test_context_data_own_items(self):
        context = self.view.get_context_data()
        self.assertIsInstance(context['items'], QuerySet)
