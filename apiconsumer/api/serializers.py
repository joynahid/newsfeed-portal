from django.db.models import fields
from rest_framework import serializers
from apiconsumer.models import SourceModel, TopHeadlineModel


class SourceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceModel
        fields = '__all__'

class TopHeadlineModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopHeadlineModel
        fields = '__all__'
