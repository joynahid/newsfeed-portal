from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db.models import fields

from user.models import UserSettings


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")

    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
    helper.form_method = "POST"


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")

    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
    helper.form_method = "POST"


class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        exclude = ['user']

    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
    helper.form_method = "POST"
