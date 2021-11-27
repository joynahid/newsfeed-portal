from django.db import models

class SourceModel(models.Model):
    id = models.AutoField(primary_key=True)
    sourceId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.CharField(max_length=255)
    country = models.CharField(max_length=100)

class TopHeadline(models.Model):
    id = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=100)
    source = models.ManyToManyField(SourceModel)
    country = models.CharField(max_length=100)