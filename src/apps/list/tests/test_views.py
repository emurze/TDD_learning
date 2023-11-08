from http import HTTPStatus

from django.urls import reverse, resolve

from apps.list.models import ListItem, List
from apps.list.tests.libs.login_test_case import LoginTestCase
from apps.list.views import HomePageView, my_list_view


class TestHomePage(LoginTestCase):
    url = '/'

    # integration
    def test_contains_start_todo(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertContains(response, '<h2>Start a new To-Do list</h2>')

    # integration
    def test_save_items_when_necessary(self) -> None:
        self.client.get(self.url)

        self.assertEqual(ListItem.objects.count(), 0)

    # integration
    def test_can_redirect_when_success(self) -> None:
        response = self.client.post(self.url, data={'content': 'Hi'})

        self.assertRedirects(
            response,
            reverse('lists', args=[f'{self.user.id}_list'])
        )

    # integration
    def test_can_show_error(self) -> None:
        response = self.client.post(self.url, data={'content': 'Hi' * 600})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, 'Ensure this value has at most 256 characters',
        )

    # integration
    def test_can_save_item(self) -> None:
        self.client.post(self.url, data={'content': 'Hi'})

        list_item = ListItem.objects.get(content='Hi')
        self.assertEqual(list_item.content, 'Hi')

    # integration
    def test_can_create_list(self) -> None:
        self.client.post(self.url, data={'content': 'Hi'})

        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(f'{self.user.id}_list', List.objects.first().slug)

    # integration
    def test_create_list_when_necessary(self) -> None:
        self.client.post(self.url, data={'content': 'Hi'})

        self.assertEqual(List.objects.count(), 1)

        self.client.post(self.url, data={'content': 'Hi'})

        self.assertEqual(List.objects.count(), 1)

    # unittest
    def test_template(self) -> None:
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home_page.html')

    # unittest
    def test_home_page_url(self) -> None:
        resolver = resolve('/')
        self.assertEqual(resolver.func.view_class, HomePageView)


class TestListView(LoginTestCase):
    @property
    def url(self) -> str:
        return f'/lists/{self.user.id}_list/'

    # integration
    def test_display_items(self) -> None:
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
    def test_can_create_items_and_list(self) -> None:
        self.client.post(self.url, data={'content': 'Vlad is car'})

        self.assertEqual(ListItem.objects.count(), 1)

        self.assertEqual(ListItem.objects.first().content, 'Vlad is car')

    # integration
    def test_can_create_items_no_list(self) -> None:
        List.objects.create(slug=f'{self.user.id}_list/')

        self.client.post(self.url, data={'content': 'Vlad is car'})

        self.assertEqual(ListItem.objects.count(), 1)

        self.assertEqual(ListItem.objects.first().content, 'Vlad is car')

    # integration
    def test_can_successfully_redirect(self) -> None:
        response = self.client.post(self.url, data={'content': 'Vlad is car'})
        self.assertRedirects(
            response, reverse('lists', args=[f'{self.user.id}_list'])
        )

    # unittest
    def test_template(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'list.html')

    # unittest
    def test_list_page_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func, my_list_view)
