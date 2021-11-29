from django.db.models import fields
from apiconsumer.api.serializers import TopHeadlineModelSerializer
from newsfeed.models import NewsFeedModel
from rest_framework import serializers


class NewsFeedSerializer(serializers.ModelSerializer):
    topHeadlines = TopHeadlineModelSerializer(many=True)

    class Meta:
        model = NewsFeedModel
        fields = "__all__"
