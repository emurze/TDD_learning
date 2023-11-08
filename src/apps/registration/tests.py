from django.contrib.auth.views import LoginView
from django.test import TestCase
from django.urls import resolve

from apps.registration.views import RegistrationView


class LoginViewTest(TestCase):
    def test_url(self) -> None:
        resolver = resolve('/login/')
        self.assertEqual(resolver.func.view_class, LoginView)


class RegistrationViewTest(TestCase):
    def test_url(self) -> None:
        resolver = resolve('/register/')
        self.assertEqual(resolver.func.view_class, RegistrationView)
