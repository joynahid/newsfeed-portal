from django.contrib import admin

from newsfeed.models import NewsFeedModel, NewsNotificationModel

admin.site.register(NewsFeedModel)
admin.site.register(NewsNotificationModel)