from django.test import TestCase

from apps.list.models import ListItem


class ListItemModel(TestCase):
    """Integration"""

    def test_creating_and_retrieving(self) -> None:
        ListItem.objects.create(content='item_1')
        ListItem.objects.create(content='item_2')

        self.assertEqual(2, ListItem.objects.count())

        item_1, item_2 = ListItem.objects.all()

        self.assertEqual(item_1.content, 'item_1')
        self.assertEqual(item_2.content, 'item_2')
