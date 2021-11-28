from typing import List
import django
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.template.base import Template
from django.template.context import Context
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from newsfeed.tasks import populate_user_newsfeed
from apiconsumer.models import SourceModel

from user.forms import LoginForm, RegistrationForm, SettingsForm
from user.models import UserSettings
from user.tasks import send_reset_password_mail, token_decode


def registration_view(req: HttpRequest):
    reg_template = loader.get_template("user/register.html")
    if req.method == "GET":
        form = RegistrationForm()

    if req.method == "POST":
        form = RegistrationForm(data=req.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                "<h1>Success</h1><p><a href='/user/login'>Login now</a></p>"
            )

    return HttpResponse(reg_template.render({"form": form}, req))

def change_password(req, token):
    try:
        decoded = token_decode(token)
        user = User.objects.get(id=decoded['userId'])

        if req.method == 'POST':
            password = req.POST.get('password')
            if password:
                user.set_password(password)
                user.save()
                return HttpResponse("Password changed successfully")

        cp_template = loader.get_template("user/change_pass.html")

        return HttpResponse(cp_template.render({'user':user}, req))
    except Exception as e:
        print(e)
        return HttpResponse("Invalid URL")

def login_view(req: HttpRequest):
    login_template = loader.get_template("user/login.html")

    if req.method == "GET":
        form = LoginForm()

    if req.method == "POST":
        form = LoginForm(data=req.POST)

        if "username" in req.POST and "password" in req.POST:
            user: User = authenticate(
                username=req.POST["username"], password=req.POST["password"]
            )

            if not user:
                raise ValidationError("wrong credentials")

            login(req, user)

            return HttpResponseRedirect("/user/profile")

    return HttpResponse(login_template.render({"form": form}, req))

def reset_password(req: HttpRequest):
    email = req.GET.get('email')

    try:
        user = User.objects.get(email=email)
        send_reset_password_mail.delay(user.id, user.email)
        return HttpResponse(f"An email was sent to {user.email}")
    except Exception:
        return HttpResponse(f"User with {email} not found")    

@login_required()
def logout(req: HttpRequest):
    return logout()


@login_required()
def profile_view(req: HttpRequest):
    profile_template = loader.get_template("user/profile.html")
    return HttpResponse(profile_template.render({"user": req.user}, req))


@login_required()
def settings_view(req: HttpRequest):
    settings_template = loader.get_template("user/settings.html")

    try:
        setting: UserSettings = UserSettings.objects.get(user=req.user)
    except Exception:
        setting = None

    choices = [(x.id, x.name) for x in SourceModel.objects.all()]

    form = SettingsForm(choices)

    if req.method == "POST":
        form = SettingsForm(choices, req.POST)

        if form.is_valid():
            countries = form.cleaned_data.get("countries")
            sources = form.cleaned_data.get("sources")
            keywords = form.cleaned_data.get("keywords")

            setting, _ = UserSettings.objects.get_or_create(
                user=req.user,
            )

            setting.countries = ",".join(countries)
            setting.keywords = keywords

            new_sources = []
            for s in sources:
                source = SourceModel.objects.get(id=s)
                new_sources.append(source)

            setting.sources.set(new_sources, clear=True)
            setting.save()

            populate_user_newsfeed.delay(req.user.id)

    if setting:
        ctx = {
            "sources": [x.id for x in setting.sources.all()],
            "countries": setting.countries.split(","),
            "keywords": setting.keywords,
        }

        form.initial = ctx

    return HttpResponse(
        settings_template.render(
            {
                "form": form,
            },
            req,
        )
    )