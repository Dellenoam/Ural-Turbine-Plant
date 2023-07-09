from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class SignInForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'id': 'username',
                'placeholder': 'Введите имя пользователя',
                'class': 'form-control',
            })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password',
                'placeholder': 'Введите пароль',
                'class': 'form-control',
            })
    )
