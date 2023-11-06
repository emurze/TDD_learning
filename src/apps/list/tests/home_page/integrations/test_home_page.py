from http import HTTPStatus

from django.test import TestCase

from apps.list.models import ListItem


class TestHomePage(TestCase):
    """Integration"""

    def test_get(self) -> None:
        response = self.client.get('/')
        html = response.content.decode('utf-8')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('<h2>Add Item</h2>', html)

    def test_post_success_redirect(self) -> None:
        response = self.client.post('/', data={'content': 'Hi'})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response['LOCATION'], '/')

    def test_post_error(self) -> None:
        response = self.client.post('/', data={'content': 'Hi' * 600})
        html = response.content.decode('utf-8')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('Ensure this value has at most 256 characters', html)

    def test_post_can_save_item(self) -> None:
        self.client.post('/', data={'content': 'Hi'})
        list_item = ListItem.objects.get(content='Hi')
        self.assertEqual(list_item.content, 'Hi')

    def test_get_save_items_when_necessary(self) -> None:
        self.client.get('/')
        self.assertEqual(ListItem.objects.count(), 0)

    def test_get_can_display_todo_items(self) -> None:
        ListItem.objects.create(content='item 2j')
        ListItem.objects.create(content='item 5j')

        response = self.client.get('/')
        html = response.content.decode('utf-8')

        self.assertIn('item 2j', html)
        self.assertIn('item 5j', html)
