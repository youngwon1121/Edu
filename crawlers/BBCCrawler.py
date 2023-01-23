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
        return [link.get_text() for link in soup.select('item > link') if "/news/" in link.get_text()][:10]

    def _parse_post(self, html):
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

    def to_site_id(self, url):
        url = urlparse(url)
        return url.path

    def get_listing_url(self):
        return self.url