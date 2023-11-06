from django.test import TestCase

from apps.list.forms import TodoCreateItemForm


class ToDoCreateItemFormTest(TestCase):
    def test_content_maxlength_constraint(self) -> None:
        form = TodoCreateItemForm(data={'content': 'New item' * 200})
        self.assertIn(
            'Ensure this value has at most 256 characters',
            str(form.errors['content']),
        )
