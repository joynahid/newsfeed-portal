from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from apiconsumer.models import TopHeadlineModel

status_choices = [
    ('ok', "OK"),
    ('fail', "Failed"),
]

class NewsFeedModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    topHeadlines = models.ManyToManyField(TopHeadlineModel)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)


class NewsNotificationModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    news = models.OneToOneField(TopHeadlineModel, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
