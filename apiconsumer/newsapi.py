from typing import Dict
import requests
from .const import *


class NewsAPIClient:
    def __init__(self, apiKey: str) -> None:
        self._apiKey = apiKey

    def _make_request(self, url: str, params: dict):
        res = requests.get(url, params=params)

        if res.status_code != 200:
            json_res = res.json()
            raise Exception(f"[{json_res['code']}] {json_res['message']}")

        return res.json()

    def sources(self, category=None, country=None, language=None):
        params = {}
        params["apiKey"] = self._apiKey
        params["category"] = category
        params["country"] = country
        params["language"] = language

        return self._make_request(SOURCE_ENDPOINT, params)

    def top_headlines(
        self,
        country=None,
        category=None,
        sources=None,
        q=None,
        pageSize=20,
        page=0,
    ) -> Dict[str, str]:
        pageSize = min(100, pageSize)

        params = {}

        params["apiKey"] = self._apiKey
        params["country"] = country
        params["category"] = category
        params["sources"] = sources
        params["q"] = q
        params["pageSize"] = pageSize
        params["page"] = page

        return self._make_request(TOP_HEADLINE_ENDPOINT, params)

    def headlines_by_country(self, country: str, pageSize=20, page=None):
        if country not in countries:
            raise ValueError(
                f'Country {country} is not available yet. Choose one of {" ".join(countries)}'
            )

        return self.top_headlines(country=country, pageSize=pageSize, page=page)

    def headlines_by_sources(self, sources=[], pageSize=20, page=None):
        return self.top_headlines(sources=sources, pageSize=pageSize, page=page)
