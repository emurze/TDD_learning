from django.test import TestCase
from django.urls import resolve

from apps.list.views import my_list_view


class ListViewTest(TestCase):
    def test_url(self) -> None:
        resolver = resolve('/lists/hi/')
        self.assertEqual(resolver.func, my_list_view)

    def test_template(self) -> None:
        pass
