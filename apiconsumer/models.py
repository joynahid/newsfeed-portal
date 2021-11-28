from django.db import models


class SourceModel(models.Model):
    id = models.AutoField(primary_key=True)
    sourceId = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.CharField(max_length=255)
    country = models.CharField(max_length=100)


class TopHeadlineModel(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    url = models.CharField(max_length=255, unique=True)
    thumbnailUrl=models.CharField(max_length=255, null=True)
    source = models.ForeignKey(SourceModel, on_delete=models.CASCADE, null=True)
    country = models.CharField(max_length=100)
    publishedAt = models.DateTimeField()

    class Meta:
        ordering = ['-publishedAt']