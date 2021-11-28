from django.contrib.auth.models import User
from user.models import UserSettings
from apiconsumer.models import SourceModel, TopHeadlineModel
from django.core.mail import send_mail, send_mass_mail
from .models import NewsFeedModel, NewsNotificationModel
from celery import shared_task
from celery.utils import log
from datetime import datetime, timedelta
import os

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


@shared_task
def notify_headlines():
    all_settings = UserSettings.objects.all()

    for setting in all_settings:
        user = setting.user

        last_notification = NewsNotificationModel.objects.filter(user=user).last()

        last_notification_send = datetime.now() - timedelta(days=30)

        if last_notification:
            last_notification_send = last_notification.createdAt

        if not setting.newsletter:
            continue

        mails = []
        for keyword in setting.keywords.split(","):
            if not keyword:
                continue

            headlines = TopHeadlineModel.objects.filter(
                description__contains=keyword,
                publishedAt__gte=last_notification_send,
            )

            print(headlines, last_notification_send)

            for headline in headlines:
                NewsNotificationModel.objects.create(
                    user=user,
                    news=headline,
                )

                message = (
                    f"Found a new news for you | Strativ News Portal.\nFind here: {headline.url}",
                    f"{headline.title}",
                    os.getenv("SEND_FROM_EMAIL"),
                    [user.email],
                )
                mails.append(message)

        number = send_mass_mail(mails)
        logger.info(f"Sent {number} emails to {user}")
