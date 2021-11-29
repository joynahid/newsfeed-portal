import os
from celery import shared_task
from celery.utils.log import get_task_logger

from user.models import UserSettings
from .models import SourceModel, TopHeadlineModel
from .newsapi import NewsAPIClient

logger = get_task_logger(__name__)


def feed_sources_sync():
    client = NewsAPIClient(os.getenv("NEWSAPI_KEY"))

    res = client.sources()

    all_sources = res["sources"]

    source_ids = set([x.sourceId for x in SourceModel.objects.all()])

    for qry in all_sources:
        if qry["id"] in source_ids:
            continue

        SourceModel.objects.create(
            sourceId=qry["id"],
            name=qry["name"],
            description=qry["description"],
            url=qry["url"],
            country=qry["country"],
        )

@shared_task
def feed_headlines_based_on_country():
    """
    Fetches news and save it to our database to serve users based on countries
    """
    countries = []
    for c in UserSettings.objects.values_list("countries", flat=True):
        countries.extend(c.split(","))

    countries = set(countries)

    logger.info(f"Gonna fetch {len(countries)} countries")

    total_created = 0
    total_heads = 0
    for c in countries:
        client = NewsAPIClient(os.getenv("NEWSAPI_KEY"))
        json = client.headlines_by_country(c)

        articles = json["articles"]

        for article in articles:
            sourceId = article["source"]["id"]
            sourceName = article["source"]["name"]

            theSource, created = SourceModel.objects.get_or_create(
                name=sourceName, country=c
            )

            total_heads += 1

            try:
                _ = TopHeadlineModel.objects.get(
                    url=article["url"].strip(),
                )
            except TopHeadlineModel.DoesNotExist as e:
                TopHeadlineModel.objects.create(
                    title=article["title"],
                    author=article["author"],
                    description=article["description"],
                    url=article["url"].strip(),
                    thumbnailUrl=article["urlToImage"],
                    source=theSource,
                    publishedAt=article["publishedAt"],
                )
                total_created += 1

    logger.info(f"Created {total_created} new Headlines out of {total_heads}")


def feed_headlines_sync():
    SOURCES_CHUNK = 20

    client = NewsAPIClient(os.getenv("NEWSAPI_KEY"))
    saved_sources = SourceModel.objects.exclude(sourceId__isnull=True)
    
    logger.info(f"Got {saved_sources.count()} sources")

    chunk_contains = saved_sources.count() // SOURCES_CHUNK + int(
        bool(saved_sources.count() % SOURCES_CHUNK)
    )

    saved_sources_list = list(saved_sources)

    source_chunks = []
    next_chunk_start = 0
    for i in range(saved_sources.count() // SOURCES_CHUNK):
        chunk_ends = min(len(saved_sources_list), (i + 1) * chunk_contains)
        source_chunks.append(saved_sources_list[next_chunk_start:chunk_ends])
        next_chunk_start += chunk_contains

    total_created = 0
    total_heads = 0
    for chunk in source_chunks:
        sources = [x.sourceId for x in chunk]
        json = client.headlines_by_sources(sources)
        total_results_number = json["totalResults"]

        PER_PAGE = 100
        total_pages = total_results_number // PER_PAGE + int(
            bool(total_results_number % PER_PAGE)
        )

        for p in range(1, total_pages + 1):
            json = client.headlines_by_sources(sources, PER_PAGE, p)
            articles = json["articles"]

            logger.info(
                f"Fetching page no. {p} out of {total_pages} pages and sources {', '.join(sources)}"
            )

            for article in articles:
                sourceId = article["source"]["id"]
                source = saved_sources.get(sourceId=sourceId)

                total_heads += 1
                try:
                    _ = TopHeadlineModel.objects.get(
                        url=article["url"].strip(),
                    )
                except TopHeadlineModel.DoesNotExist as e:
                    TopHeadlineModel.objects.create(
                        title=article["title"],
                        author=article["author"],
                        description=article["description"],
                        url=article["url"].strip(),
                        thumbnailUrl=article["urlToImage"],
                        source=source,
                        publishedAt=article["publishedAt"],
                    )

                    total_created += 1

    logger.info(f"Created {total_created} new Headlines out of {total_heads}")


@shared_task
def feed_sources():
    """
    Fetches sources from newsapi and saves it in the database
    """
    feed_sources_sync()


@shared_task
def feed_headlines():
    """
    Fetches headlines by sources and saves into database
    """
    feed_headlines_sync()
