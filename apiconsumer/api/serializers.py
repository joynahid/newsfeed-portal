from django.db.models import fields
from rest_framework import serializers
from apiconsumer.models import SourceModel


class SourceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceModel
        fields = '__all__'
