from django.contrib.auth.models import User
from user.models import UserSettings
from apiconsumer.models import SourceModel, TopHeadlineModel
from .models import NewsFeedModel
from celery import shared_task
from celery.utils import log

logger = log.get_logger(__name__)


def feed(user):
    setting: UserSettings = UserSettings.objects.get(user=user)

    preferred_sources = list(setting.sources.all())
    preferred_sources += list(
        SourceModel.objects.filter(country__in=setting.countries.split(","))
    )

    headlines = TopHeadlineModel.objects.filter(source__in=preferred_sources)

    newsfeed, created = NewsFeedModel.objects.get_or_create(user=user)

    newsfeed.topHeadlines.set(headlines)


def populate_newsfeed_sync():
    users = User.objects.all()

    for user in users:
        feed(user)


@shared_task
def populate_newsfeed():
    populate_newsfeed_sync()


@shared_task
def populate_user_newsfeed(userId):
    feed(User.objects.get(id=userId))
