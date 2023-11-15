from http import HTTPStatus
from unittest import TestCase

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.list.forms import TodoCreateItemForm, EMPTY_ITEM_ERROR, \
    TodoEmailForm, EMAIL_INVALID_ERROR
from apps.list.models import ListItem, List
from apps.list.tests.libs.login_test_case import LoginTestCase


class ToDoCreateItemFormTest(TestCase):
    form_required_error: str = EMPTY_ITEM_ERROR

    # unittest
    def test_cannot_create_without_list(self) -> None:
        with self.assertRaises(IntegrityError):
            form = TodoCreateItemForm(data={'content': 'Hi god!'})
            form.save()

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


class TodoEmailFormTest(TestCase):
    form_required_error: str = EMPTY_ITEM_ERROR
    form_email_error: str = EMAIL_INVALID_ERROR

    # unittest
    def test_form_email_null_constraint(self) -> None:
        email_form = TodoEmailForm(data={'email': ''})
        self.assertFalse(email_form.is_valid())
        self.assertIn(
            self.form_required_error,
            email_form.errors['email'],
        )

    # unittest
    def test_form_email_constraint(self) -> None:
        email_form = TodoEmailForm(data={'email': 'hide_yourself'})
        self.assertFalse(email_form.is_valid())
        self.assertIn(
            self.form_email_error,
            email_form.errors['email'],
        )
