from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class LoginTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='vlad', password='146080ce'
        )
        self.client.login(username='vlad', password='146080ce')
