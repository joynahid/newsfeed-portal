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
    """
    Sends email to user based last sent email.
    It won't send any email before the last news publish time
    """
    all_settings = UserSettings.objects.all()

    for setting in all_settings:
        user = setting.user

        last_notification = NewsNotificationModel.objects.filter(user=user).last()

        last_notification_send = datetime.now() - timedelta(days=30)

        if last_notification:
            last_notification_send = last_notification.news.publishedAt
            logger.info("Last news published at", last_notification.news.publishedAt)

        if not setting.newsletter:
            continue

        mails = []
        for keyword in setting.keywords.split(","):
            if not keyword:
                continue

            headlines = TopHeadlineModel.objects.filter(
                description__icontains=keyword,
                publishedAt__gt=last_notification_send,
            ) | TopHeadlineModel.objects.filter(
                title__icontains=keyword,
                publishedAt__gt=last_notification_send,
            )

            headline = headlines.first()

            logger.info(f"Found {headlines.count()} headlines for {keyword}")

            if not headline:
                continue

            NewsNotificationModel.objects.create(
                user=user,
                news=headline,
            )

            message = (
                f"Found a new news for you | Strativ News Portal",
                f"Hi {user.username}! We got a new headline for you.\n\n{headline.title}\n\nFind it here {headline.url}",
                os.getenv("SEND_FROM_EMAIL"),
                [user.email],
            )

            mails.append(message)

        logger.info(f"{len(mails)} mails are ready to send")

        number = send_mass_mail(mails, fail_silently=False)
        logger.info(f"Sent {number} emails to {user}")
