import enum
from collections.abc import Callable

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase, RequestFactory

User = get_user_model()


class Method(enum.Enum):
    GET = 'get'
    POST = 'post'


class LoginTestCase(TestCase):
    url: str
    func: Callable

    """
    Requirements for make_request:
        - url: str
        - func: Callable
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username='vlad', password='146080ce'
        )

    def setUp(self):
        self.client.login(username='vlad', password='146080ce')

    def make_request(self, method: Method, data: dict | None = None) -> HttpResponse:
        _method: Callable = getattr(self.factory, method.value)
        _method(self.url)
        return self.func(**data)
