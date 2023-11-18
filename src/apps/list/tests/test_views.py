import json
from collections.abc import Callable

from http import HTTPStatus
from unittest.mock import patch, MagicMock, call

from django.urls import reverse, resolve, reverse_lazy

from apps.list.domain import JsonStatus
from apps.list.forms import EMPTY_ITEM_ERROR, TodoCreateItemForm, TodoEmailForm
from apps.list.models import ListItem, List
from apps.list.tests.libs.login_test_case import LoginTestCase, Method
from apps.list.views import HomePageView, my_list_view, send_email, \
    custom_login
from utils import mixin_for
from django.test import RequestFactory


class CreateItemFormTestMixin(mixin_for(LoginTestCase)):
    """
    Require:
        - url: str
        - base_template: str
    """
    url: str
    base_template: str
    form_required_error: str = EMPTY_ITEM_ERROR
    form_maxlength_error: str = 'Ensure this value has at most 256 characters'

    # integration
    def test_form_invalid_not_saved_item(self) -> None:
        self.factory.post(self.url, data={'content': 'Hi' * 600})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(ListItem.objects.count(), 0)

    # integration
    def test_form_invalid_show_maxlength_error(self) -> None:
        response = self.client.post(self.url, data={'content': 'Hi' * 600})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.form_maxlength_error)

    # integration
    def test_form_invalid_show_null_error(self) -> None:
        response = self.client.post(self.url, data={'content': ''})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.form_required_error)

    # integration
    def test_form_invalid_template(self) -> None:
        response = self.client.post(self.url, data={'content': ''})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.base_template)

    # integration
    def test_form_valid_can_create_items_and_list(self) -> None:
        self.client.post(self.url, data={'content': 'Vlad is car'})

        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(ListItem.objects.count(), 1)
        self.assertEqual(ListItem.objects.first().content, 'Vlad is car')

    # integration
    def test_form_valid_can_create_items_without_list(self) -> None:
        List.objects.create(slug=f'{self.user.id}_list/')

        self.client.post(self.url, data={'content': 'Vlad is car'})

        self.assertEqual(ListItem.objects.count(), 1)
        self.assertEqual(ListItem.objects.first().content, 'Vlad is car')

    # integration
    def test_form_valid_can_redirect(self) -> None:
        response = self.client.post(self.url, data={'content': 'Vlad is car'})
        self.assertRedirects(
            response, reverse('lists', args=[f'{self.user.id}_list'])
        )

    # integration
    def test_form_valid_cannot_duplicate_two_lists(self) -> None:
        self.client.post(self.url, data={'content': 'Vlad is car'})

        self.assertEqual(List.objects.count(), 1)

        self.client.post(self.url, data={'content': 'Vlad is car'})

        self.assertEqual(List.objects.count(), 1)

    # integration
    def test_get_cannot_show_error(self) -> None:
        response = self.client.get(self.url)
        self.assertNotContains(response, self.form_required_error)

    # integration
    def test_get_cannot_save_items(self) -> None:
        self.client.get(self.url)
        self.assertEqual(ListItem.objects.count(), 0)

    # integration
    def test_form_class(self) -> None:
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], TodoCreateItemForm)


class TestHomePage(CreateItemFormTestMixin, LoginTestCase):
    url: str = reverse_lazy('home_page')
    base_template: str = 'list/home_page.html'
    page_header: str = 'Create To-Do list'
    func: Callable = HomePageView.as_view()

    # integration
    def test_get_show_start_todo(self) -> None:
        response = self.make_request(Method.POST)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.page_header)

    # integration
    def test_form_valid_create_list(self) -> None:
        self.make_request(Method.POST, data={'content': 'Hi'})

        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(f'{self.user.id}_list', List.objects.first().slug)

    # integration
    def test_email_form(self) -> None:
        response = self.make_request(Method.POST)
        self.assertIsInstance(
            response.context['email_form'],
            TodoEmailForm,
        )

    # integration
    def test_email_form_action(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(
            response.context['email_form_action'],
            reverse_lazy('send_email'),
        )

    # unittest
    def test_template(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.base_template)

    # unittest
    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func.view_class, HomePageView)


class TestListView(CreateItemFormTestMixin, LoginTestCase):
    page_header: str = 'Your To-Do list'
    base_template: str = 'list/list.html'

    @property
    def slug(self) -> str:
        return f'{self.user.id}_list'

    @property
    def url(self) -> str:
        return reverse_lazy('lists', args=(f'{self.user.id}_list',))

    # integration
    def test_get_show_your_todo(self) -> None:
        request = self.factory.get(self.url)
        request.user = self.user
        response = my_list_view(request, self.slug)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.page_header)

    # integration
    def test_get_show_items(self) -> None:
        new_list = List.objects.create(slug=f'{self.user.id}_list')
        ListItem.objects.create(content='item 1', list=new_list)
        ListItem.objects.create(content='item 2', list=new_list)
        ListItem.objects.create(content='item 3', list=new_list)

        request = self.factory.get(self.url)
        request.user = self.user
        response = my_list_view(request, self.slug)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertContains(response, 'item 3')

    # integration
    def test_template(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.base_template)

    # integration
    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func, my_list_view)

    @patch('apps.list.views.List')
    @patch('apps.list.views.TodoCreateItemForm')
    def test_form_valid_can_create_new_list_with_slug11(
            self, mock_form: MagicMock, mock_list: MagicMock,
    ) -> None:
        request = self.factory.post(self.url, data={'content': 'Hi'}, )
        request.user = self.user

        my_list_view(request, f'{self.user.id}_list')

        new_list = mock_list.return_value
        user_slug = f'{self.user.id}_list'

        self.assertEqual(new_list.slug, user_slug)


class SendEmailViewTest(LoginTestCase):
    url = reverse_lazy('send_email')
    func = send_email

    def get_form_invalid_response(self) -> dict:
        response = self.make_request(Method.POST, data={'email': 'hi'})
        return dict(
            json.loads(
                response.content.decode('utf-8')
            )
        )

    def get_form_valid_response(self, email: str = 'adm1@amd1.com') -> dict:
        response = self.make_request(Method.POST, data={'email': email})
        return dict(
            json.loads(
                response.content.decode('utf-8')
            )
        )

    # integration
    @patch('apps.list.views.send_mail')
    def test_post_form_valid_send_mail(self, mock_send_mail: MagicMock,) -> None:
        dict_response = self.get_form_valid_response(email='lerka@gmail.com')
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

        self.assertEqual(dict_response.get('status'), JsonStatus.OK)
        self.assertTrue(mock_send_mail.called)
        self.assertEqual(subject, 'Your login link for SuperLists')
        self.assertEqual(body, 'body text tbc')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['lerka@gmail.com'])

    # integration
    @patch('apps.list.views.messages')
    @patch('apps.list.views.send_mail')
    def test_form_valid_success_message(
            self,
            mock_send_mail: MagicMock,
            mock_messages: MagicMock,
    ) -> None:
        response: dict = self.get_form_valid_response(email='lerka@gmail.com')
        self.assertEqual(response['status'], JsonStatus.OK)
        self.assertEqual(
            mock_messages.success.call_args[0][1],
            'Email message was successfully sent',
        )

    # integration
    def test_post_form_invalid(self) -> None:
        response: dict = self.get_form_invalid_response()
        self.assertEqual(response['status'], JsonStatus.ERROR)
        self.assertIn('Enter a valid email address', response['error_message'])

    # integration
    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func, send_email)


class CustomLoginTest(LoginTestCase):
    url: str = '/custom_login'
    func: Callable = custom_login
    """Write 3 tests instead of mock"""

    @patch('apps.list.views.auth')
    def test_custom_login_the_same_user(self, mock_auth: MagicMock) -> None:
        """Depends on implementation"""

        self.make_request(Method.GET)
        request = RequestFactory().get('/custom_login')
        request.user = self.user

        custom_login(request)

        self.assertEqual(
            mock_auth.login.call_args,
            call(request, mock_auth.authenticate.return_value)
        )
