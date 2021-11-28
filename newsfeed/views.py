from django.http.response import HttpResponse
from django.shortcuts import render
from django.http.request import HttpRequest
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import NewsFeedModel


@login_required
def newsfeedindex(req: HttpRequest):
    """
    Returns updated newsfeed to the requested user
    Two parameters can be provided, one is offset and other is limit.
    For example: /?offset=0&limit=20

    Note: limit can be max 20
    """
    offset = req.GET.get("offset")
    if not offset:
        offset = 0

    offset = int(offset)

    limit = req.GET.get("limit")

    if not limit:
        limit = 20

    limit= int(limit)

    limit = min(limit, 20)

    feed = NewsFeedModel.objects.get(user=req.user)

    headlines = feed.topHeadlines.all()
    cnt = headlines.count()

    end = min(offset + limit, cnt)

    headlines = headlines[offset:end]

    template = loader.get_template("newsfeed/index.html")

    if offset +10 >= cnt:
        offset = -1

    return HttpResponse(
        template.render({"top_headlines": headlines, "offset": offset}, req)
    )
