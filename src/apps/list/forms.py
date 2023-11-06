from django import forms

from apps.list.models import ListItem


class TodoCreateItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ('content',)
