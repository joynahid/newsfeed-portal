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

from user.forms import LoginForm, RegistrationForm, SettingsForm


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


@login_required()
def logout(req: HttpRequest):
    return logout()


@login_required()
def profile_view(req: HttpRequest):
    profile_template = loader.get_template("user/profile.html")
    return HttpResponse(profile_template.render({"user": req.user}, req))


@login_required()
def settings_view(req):
    settings_template = loader.get_template("user/settings.html")
    form = SettingsForm()
    return HttpResponse(settings_template.render({"form": form}, req))
