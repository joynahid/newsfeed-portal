from django.contrib import admin
from django.urls import path, include

from .views import NewsFeedView

urlpatterns = [
    path('', NewsFeedView.as_view(), name="newsfeed_api"),
]
