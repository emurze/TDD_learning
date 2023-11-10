import datetime

from django.test import TestCase

from django.db import IntegrityError

from apps.list.models import ListItem, List


class ListAndItemsModelTest(TestCase):
    def setUp(self) -> None:
        self.new_list = List.objects.create(slug='some')

    # integration
    def test_creating_and_retrieving(self) -> None:
        ListItem.objects.create(content='item_1', list=self.new_list)
        ListItem.objects.create(content='item_2', list=self.new_list)

        self.assertEqual(2, ListItem.objects.count())

        item_1, item_2 = ListItem.objects.all()

        self.assertEqual(item_1.content, 'item_1')
        self.assertEqual(item_2.content, 'item_2')

    # integration
    def test_item_not_null(self) -> None:
        with self.assertRaises(IntegrityError):
            ListItem.objects.create(content=None, list=self.new_list)

    # integration
    def test_fk_list_rel(self) -> None:
        item = ListItem.objects.create(content='item_1', list=self.new_list)
        self.assertEqual(item.list, self.new_list)


class ListModelTest(TestCase):
    # integration
    def test_creating_retrieving(self) -> None:
        List.objects.create(slug='hi_world')
        my_list = List.objects.get(slug='hi_world')

        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(my_list.slug, 'hi_world')

    # integration
    def test_unique_slug(self) -> None:
        List.objects.create(slug='item_1')
        try:
            List.objects.create(slug='item_1')
            self.assertTrue(0)
        except IntegrityError:
            self.assertTrue(1)

    # integration
    def test_created_is_not_null(self) -> None:
        item = List.objects.create(slug='item_1')
        self.assertIsInstance(item.created, datetime.date)
        self.assertIsNotNone(item.created)

    # integration
    def test_ordering(self) -> None:
        self.assertTrue(List.objects.all().ordered)

    # integration
    def test_get_absolute_url(self) -> None:
        new_list = List.objects.create(slug='hi')
        self.assertEqual(
            new_list.get_absolute_url(),
            f'/lists/{new_list.slug}/'
        )
