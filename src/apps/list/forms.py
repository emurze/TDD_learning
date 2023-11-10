from django import forms

from apps.list.models import ListItem

EMPTY_ITEM_ERROR = "You cannot create an empty list item"


class TodoCreateItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'content': {'required': EMPTY_ITEM_ERROR}
        }
