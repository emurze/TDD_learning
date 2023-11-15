import json

from http import HTTPStatus

from django.urls import reverse, resolve, reverse_lazy

from apps.list.domain import JsonStatus
from apps.list.forms import EMPTY_ITEM_ERROR, TodoCreateItemForm, TodoEmailForm
from apps.list.models import ListItem, List
from apps.list.tests.libs.login_test_case import LoginTestCase
from apps.list.views import HomePageView, my_list_view, send_email
from utils import mixin_for

import apps.list.views


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
        self.client.post(self.url, data={'content': 'Hi' * 600})
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

    # integration
    def test_get_show_start_todo(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.page_header)

    # integration
    def test_form_valid_create_list(self) -> None:
        self.client.post(self.url, data={'content': 'Hi'})

        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(f'{self.user.id}_list', List.objects.first().slug)

    # integration
    def test_email_form(self) -> None:
        response = self.client.get(self.url)
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
    def url(self) -> str:
        return reverse_lazy('lists', args=(f'{self.user.id}_list',))

    # integration
    def test_get_show_your_todo(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.page_header)

    # integration
    def test_get_show_items(self) -> None:
        new_list = List.objects.create(slug=f'{self.user.id}_list')
        ListItem.objects.create(content='item 1', list=new_list)
        ListItem.objects.create(content='item 2', list=new_list)
        ListItem.objects.create(content='item 3', list=new_list)

        response = self.client.get(self.url)

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


class SendEmailViewTest(LoginTestCase):
    url = reverse_lazy('send_email')

    """Data from fake_send_mail"""
    send_mail_called: bool
    subject: str
    body: str
    from_email: str
    to_list: list[str] | tuple[str]

    def get_form_invalid_response(self) -> dict:
        response = self.client.post(self.url, data={'email': 'hi'})
        return dict(
            json.loads(
                response.content.decode('utf-8')
            )
        )

    def get_form_valid_response(self, email: str = 'adm1@amd1.com') -> dict:
        response = self.client.post(self.url, data={'email': email})
        return dict(
            json.loads(
                response.content.decode('utf-8')
            )
        )

    # integration
    def test_post_form_valid_send_mail(self) -> None:
        self.send_mail_called = False

        def fake_send_mail(
            subject: str,
            body: str,
            from_email: str,
            to_list: list[str] | tuple[str],
        ) -> None:
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        apps.list.views.send_mail = fake_send_mail

        dict_response = self.get_form_valid_response(
            email='hi_lerka@gmail.com',
        )

        self.assertEqual(dict_response.get('status'), JsonStatus.OK)
        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for SuperLists')
        self.assertEqual(self.body, 'body text tbc')
        self.assertEqual(self.from_email, 'noreply@superlists')
        self.assertEqual(self.to_list, ['hi_lerka@gmail.com'])

    # integration
    def test_post_form_invalid(self) -> None:
        dict_response = self.get_form_invalid_response()
        self.assertEqual(dict_response.get('status'), JsonStatus.ERROR)

    # integration
    def test_get_is_not_allowed(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    # integration
    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func, send_email)
