from main.models import KekPass
from typing import Any

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, Submit, Hidden
from django.contrib.auth import forms as auth_forms
from django import forms
from django.http import HttpRequest
from django.urls import reverse
from django_registration import forms as registration_forms


class RegistrationForm(registration_forms.RegistrationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1']:
            self.fields[fieldname].help_text = None
        self.fields.pop('email')
        self.fields.pop('password2')
        self.helper = FormHelper(self)
        self.helper.form_show_errors = False
        self.helper.form_action = reverse('register')
        self.helper.layout = Layout(
            FloatingField('username'),
            FloatingField('password1'),
            ButtonHolder(Submit('submit', 'Зарегистрироваться')),
        )


class AuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().__init__(request=request, *args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_errors = False
        self.helper.layout = Layout(
            FloatingField('username'),
            FloatingField('password'),
            ButtonHolder(Submit('submit', 'Войти')),
        )


class KekPassForm(forms.ModelForm):
    class Meta:
        model = KekPass
        fields = ['host', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            FloatingField('host'),
            FloatingField('password',  style='font-family: monospace'),
            ButtonHolder(Submit('submit', 'Сохранить')),
        )
