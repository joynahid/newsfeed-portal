from django.urls import path
from .views import ChangePassword, InitiateChangePassword, LoginUser, Profile, RegisterUser, UserSettingsAPI

urlpatterns = [
    path("registration", RegisterUser.as_view(), name='registration_api'),
    path("login", LoginUser.as_view(), name='login_api'),
    path("change_password/<str:token>", ChangePassword.as_view(), name="change_password_api"),
    path("initiate_change_password", InitiateChangePassword.as_view(), name="initiate_change_password_api"),
    path("profile", Profile.as_view(), name="profile_api"),
    path("settings", UserSettingsAPI.as_view(), name="user_settings_api")
]