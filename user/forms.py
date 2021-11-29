from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.widgets import PasswordInput

from apiconsumer.const import *
import pycountry


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=PasswordInput,
        max_length=100,
        min_length=8,
        help_text="Minimum 8 characters",
    )
    email = forms.EmailField(help_text="Must be a valid email")

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def save(self, commit=True):
        instance = super(RegistrationForm, self).save(commit=False)

        user = User.objects.create_user(
            instance.username,
            instance.email,
            instance.password,
        )

        return user

    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
    helper.form_method = "POST"


class LoginForm(forms.ModelForm):
    password = forms.CharField(
        widget=PasswordInput,
        max_length=100,
        min_length=8,
        help_text="Minimum 8 characters",
    )

    class Meta:
        model = User
        fields = ("username", "password")

    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
    helper.form_method = "POST"


class SettingsForm(forms.Form):
    def __init__(self, choices, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields["sources"] = forms.MultipleChoiceField(
            label="Sources",
            required=False,
            choices=choices,
            widget=forms.CheckboxSelectMultiple,
        )

    keywords = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Comma separated keyword list. You'll be notified in your email based on these configurations"
            }
        ),
        help_text="Write keywords separated by comma",
    )

    countries = forms.MultipleChoiceField(
        label="Countries",
        choices=[
            (
                x,
                pycountry.countries.get(alpha_2=x).name
                if pycountry.countries.get(alpha_2=x)
                else x,
            )
            for x in countries
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit"))
    helper.form_method = "POST"
