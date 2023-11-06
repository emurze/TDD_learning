from django.test import TestCase
from django.urls import resolve

from apps.list.views import HomePageView


class TestHomePageView(TestCase):
    """Unittest"""

    def test_url(self) -> None:
        resolver = resolve('/')
        self.assertEqual(resolver.func.view_class, HomePageView)

    def test_template(self) -> None:
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home_page.html')
