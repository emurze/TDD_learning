import logging

from django.test import TestCase
from django.urls import resolve

from apps.list.models import TodoItem
from apps.list.views import todo_page_view

lg = logging.getLogger(__name__)


class TodoPageTest(TestCase):
    def test_mapping_func_to_url(self) -> None:
        found = resolve('/')
        self.assertEqual(found.func, todo_page_view)

    def test_template_existence(self) -> None:
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'list/todo.html')

    def test_only_saves_items_when_necessary(self) -> None:
        self.client.get('/')
        self.assertEqual(TodoItem.objects.count(), 0)

    def test_can_create_new_todo_item(self) -> None:
        self.client.post('/', data={'content': 'New item'})

        self.assertEqual(TodoItem.objects.count(), 1)
        self.assertEqual(TodoItem.objects.first().content, 'New item')

    def test_can_redirect_todo_item(self) -> None:
        response = self.client.post('/', data={'content': 'New item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_page_can_display_multiple_items(self) -> None:
        first_item = TodoItem.objects.create(content='Item 1')
        second_item = TodoItem.objects.create(content='Item 2')

        response = self.client.get('/')

        self.assertIn(first_item.content, response.content.decode('utf-8'))
        self.assertIn(second_item.content, response.content.decode('utf-8'))
