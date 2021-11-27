from django.urls import path
from .views import login_view, profile_view, registration_view, settings_view

urlpatterns = [
    path("registration", registration_view),
    path("login", login_view),
    path("profile", profile_view, name="login"),
    path("settings", settings_view)
]