from http import HTTPStatus

from django.urls import reverse, resolve

from apps.list.forms import EMPTY_ITEM_ERROR, TodoCreateItemForm
from apps.list.models import ListItem, List
from apps.list.tests.libs.login_test_case import LoginTestCase
from apps.list.views import HomePageView, my_list_view
from utils import mixin_for


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
    url: str = '/'
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
        return f'/lists/{self.user.id}_list/'

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

    # unittest
    def test_template(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.base_template)

    # unittest
    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func, my_list_view)
