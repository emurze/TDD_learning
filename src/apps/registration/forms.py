import logging

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
lg = logging.getLogger(__name__)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat password',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                "autofocus": True,
                'placeholder': 'Username'
            }),
        }

    def clean_username(self) -> str:
        cd = self.cleaned_data

        username = cd.get('username')
        if len(username) > 25:
            raise forms.ValidationError('Username should be less then 26')

        return username

    def clean_password2(self):
        cd = self.cleaned_data

        if cd.get('password2') != cd.get('password'):
            raise forms.ValidationError("Passwords didn't match.")

        if len(cd.get('password2')) < 8:
            raise forms.ValidationError("Passwords length less than 8")

        return cd.get('password2')