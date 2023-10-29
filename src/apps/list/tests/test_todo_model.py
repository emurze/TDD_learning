from django.test import TestCase

from apps.list.models import TodoItem


class TodoModelTest(TestCase):
    def test_todo_item_creating_and_retrieving(self) -> None:
        TodoItem.objects.bulk_create([
            TodoItem(content='item 1'),
            TodoItem(content='item 2')
        ])

        item_1, item_2 = TodoItem.objects.order_by('content')

        self.assertEqual(item_1.content, 'item 1')
        self.assertEqual(item_2.content, 'item 2')
