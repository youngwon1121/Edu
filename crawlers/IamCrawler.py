import json
import zoneinfo
from typing import List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.utils import timezone

from crawlers.BaseCrawler import RequestCrawler


class IamCrawler(RequestCrawler[dict]):
    def __init__(self, url=None):
        super().__init__(url)
        self.site = "IAM"

    def get_listing_url(self):
        url = urlparse(self.url)
        return url._replace(path='/api/article' + url.path).geturl()

    def _parse_index(self, json_data) -> List[dict]:
        json_data = json.loads(json_data)
        return json_data['articles'][:10]

    def _parse_post(self, html, data: dict):
        article = data
        soup = BeautifulSoup(html, 'html.parser')

        js = soup.select_one("#__content script").get_text(strip=True)
        start = "toHtml("
        end = ");"
        start_index = js.find(start) + len(start)
        end_index = js.find(end)
        content = str(json.loads(js[start_index:end_index]))

        published_datetime = timezone.datetime.strptime(article['reg_date'], '%Y-%m-%d %H:%M:%S').replace(
            tzinfo=zoneinfo.ZoneInfo("Asia/Seoul"))

        file = []
        if article['files'] is not None:
            file = [file['title'] for file in article['files']]
        return {
            'url': article['view_link'],
            'site': self.site,
            'site_id': article['id'],
            'title': article['title'],
            'body': content,
            'published_datetime': published_datetime,
            'attachment_list': file
        }

    def site_id_from_data(self, data: dict) -> str:
        return str(data['id'])

    def url_from_data(self, data: dict):
        return data['view_link']
