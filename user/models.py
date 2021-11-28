from django.core.exceptions import ValidationError
from django.db import models

from django.contrib.auth.models import User
from apiconsumer.const import countries
from apiconsumer.models import SourceModel

def one_of_these_countries(value):
    if value not in countries:
        raise ValidationError(f"{value} is not valid", params={"country": value})

class UserSettings(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    countries = models.TextField()
    sources = models.ManyToManyField(SourceModel)
    keywords = models.TextField()