import os
from celery import Celery
from celery.signals import worker_ready

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsportal.settings")
app = Celery("newsportal")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "feed-news-every-15-minutes": {
        "task": "apiconsumer.tasks.feed_headlines",
        "schedule": 60*15,
    },
    "sync-sources-every-24-hours": {
        "task": "apiconsumer.tasks.feed_sources",
        "schedule": 24*60*60,
    },
    "sync-newsfeed-every-15-minutes": {
        "task": "newsfeed.tasks.populate_newsfeed",
        "schedule": 15*60,
    },
    "notify-user-every-30-minutes": {
        "task": "newsfeed.tasks.notify_headlines",
        "schedule": 30*60,
    },
}

app.autodiscover_tasks()