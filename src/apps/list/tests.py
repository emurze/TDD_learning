import logging

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from apps.list.views import home_page_view

lg = logging.getLogger(__name__)


class HomePageTest(TestCase):
    def test_root_resolves_to_home_page_view(self) -> None:
        found_url = resolve('/')
        self.assertEqual(found_url.func, home_page_view)

    def test_home_page_returns_correct_html(self) -> None:
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'list/home_page.html')
