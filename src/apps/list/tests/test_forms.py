from http import HTTPStatus
from unittest import TestCase

from apps.list.forms import TodoCreateItemForm, EMPTY_ITEM_ERROR
from apps.list.tests.libs.login_test_case import LoginTestCase


class ToDoCreateItemFormTest(LoginTestCase):
    form_required_error: str = EMPTY_ITEM_ERROR

    # unittest
    def test_content_maxlength_constraint(self) -> None:
        form = TodoCreateItemForm(data={'content': 'New item' * 200})
        self.assertIn(
            'Ensure this value has at most 256 characters',
            str(form.errors['content']),
        )

    # unittest
    def test_form_content_placeholder(self) -> None:
        form = TodoCreateItemForm(data={'content': 'New item'})
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    # unittest
    def test_form_content_classes(self) -> None:
        form = TodoCreateItemForm(data={'content': 'New item'})
        self.assertIn('class="form-control', form.as_p())

    # unittest
    def test_form_content_null_constraint(self) -> None:
        form = TodoCreateItemForm(data={'content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn(self.form_required_error, form.errors['content'])
