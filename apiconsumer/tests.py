import os
from django.test import TestCase
from unittest import mock

from apiconsumer.newsapi import NewsAPIClient

sample_res = {
    "status": "ok",
    "totalResults": 38,
    "articles": [
        {
            "source": {"id": "nbc-news", "name": "NBC News"},
            "author": "Charlene Gubash, Petra Cahill",
            "title": "Egypt to reopen ancient Avenue of Sphinxes in with Luxor parade - NBC News",
            "description": "Egypt is set to reopen the 3,000-year-old Avenue of the Sphinxes Thursday with a Thanksgiving Day parade of its own in Luxor.",
            "url": "https://www.nbcnews.com/news/world/egypt-reopen-ancient-avenue-sphinxes-luxor-karnak-parade-rcna6723",
            "urlToImage": "https://media-cldnry.s-nbcnews.com/image/upload/t_nbcnews-fp-1200-630,f_auto,q_auto:best/rockcms/2021-11/211125-avenue-of-sphinxes-mb-1512-7b5e7d.jpg",
            "publishedAt": "2021-11-25T18:34:58Z",
            "content": "CAIRO As Americans feast their eyes on a full-blown Thanksgiving Day parade after a two-year Covid absence, nearly 6,000 miles away Egypt is set to revive a very different cultural tradition that has… [+4072 chars]",
        },
        {
            "source": {"id": "usa-today", "name": "USA Today"},
            "author": "Jennifer Ernst Beaudry, Elsie Boskamp and James Aitchison, USA TODAY",
            "title": "We're live tracking 300+ best deals to shop this Black Friday from Walmart, Target, Best Buy and more - USA TODAY",
            "description": "Shop the best Black Friday 2021 deals around—we've got your roundup of all the best deals from Target, Walmart, Amazon and more.",
            "url": "https://www.usatoday.com/story/money/reviewed/2021/11/25/black-friday-deals-2021-epic-deals-walmart-amazon-and-more/6049106001/",
            "urlToImage": "https://www.gannett-cdn.com/presto/2021/11/24/USAT/8a213d02-97af-4c70-ac01-dff06f08e6f4-2021_11_24_DEALS_BlackFriday_Hero.png?auto=webp&crop=2987,1681,x6,y0&format=pjpg&width=1200",
            "publishedAt": "2021-11-25T18:32:54Z",
            "content": "— Recommendations are independently chosen by Reviewed’s editors. Purchases you make through our links may earn us a commission.\r\nIt's the moment shoppers have been waiting for: Black Friday 2021 has… [+20753 chars]",
        },
    ],
}


def mocked_make_requests(*args, **kwargs):
    class Response:
        status_code: int

        def __init__(self, status_code: int, data: dict) -> None:
            self.status_code = status_code
            self.data = data

        def json(self):
            return self.data

    return Response(200, sample_res)


class ApiConsumerTest(TestCase):
    @mock.patch("requests.get", side_effect=mocked_make_requests)
    def test_top_headlines(self, mck):
        napi = NewsAPIClient("secretapikey")
        json_res = napi.top_headlines("us")

        self.assertEqual(json_res["status"], "ok")
        self.assertEqual(json_res["totalResults"], 38)
