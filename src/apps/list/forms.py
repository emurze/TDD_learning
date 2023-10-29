from django import forms

from apps.list.models import TodoItem


class CreateTodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Enter new item name',
            })
        }
