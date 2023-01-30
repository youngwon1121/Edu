import datetime
import zoneinfo
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from crawlers.BaseCrawler import RequestCrawler


class BBCCrawler(RequestCrawler):

    def __init__(self, url):
        super().__init__(url)
        self.site = "BBC"

    def _parse_index(self, xml):
        soup = BeautifulSoup(xml, "xml")
        items = [item for item in soup.select('item') if "/news/" in item.get_text()]
        items.sort(key=lambda i: datetime.datetime.strptime(i.select_one("pubDate").get_text(), "%a, %d %b %Y %H:%M:%S %Z"), reverse=True)
        return [item.select_one('guid').get_text() for item in items][:10]

    def _parse_post(self, html, data=None):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find("h1", id="main-heading").get_text(strip=True)
        body = "".join(map(str, soup.select("article > div")))

        published_datetime = soup.select_one("header time")['datetime']
        published_datetime = timezone.datetime.strptime(published_datetime, '%Y-%m-%dT%H:%M:%S.%fZ').replace(
            tzinfo=zoneinfo.ZoneInfo("UTC"))
        return {
            'title': title,
            'body': body,
            'published_datetime': published_datetime,
            'attachment_list': []
        }

    def site_id_from_data(self, data):
        data = urlparse(data)
        return data.path

    def get_listing_url(self):
        return self.url