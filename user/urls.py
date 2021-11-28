from django.urls import path
from .views import login_view, profile_view, registration_view, reset_password, settings_view, change_password

urlpatterns = [
    path("registration", registration_view),
    path("login", login_view),
    path("reset_password", reset_password),
    path("change_password/<str:token>", change_password),
    path("profile", profile_view, name="login"),
    path("settings", settings_view)
]