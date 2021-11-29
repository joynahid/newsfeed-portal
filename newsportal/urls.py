from django.contrib import admin
from django.urls import path, include

from newsfeed.views import newsfeedindex

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('api/user/', include('user.api.endpoints')),
    path('api/newsfeed/', include('newsfeed.api.endpoints')),
    path('', newsfeedindex)
]
