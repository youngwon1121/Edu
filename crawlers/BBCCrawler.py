import datetime
import zoneinfo
from typing import List
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag

from crawlers.BaseCrawler import RequestCrawler


class BBCCrawler(RequestCrawler[Tag]):

    def __init__(self, url):
        super().__init__(url)
        self.site = "BBC"

    def _parse_index(self, xml) -> List[Tag]:
        soup = BeautifulSoup(xml, "xml")
        items = [item for item in soup.select('item') if "/news/" in item.get_text()]
        items.sort(key=lambda i: datetime.datetime.strptime(i.select_one("pubDate").get_text(), "%a, %d %b %Y %H:%M:%S %Z"), reverse=True)
        return items[:10]

    def _parse_post(self, html, data: Tag):
        soup = BeautifulSoup(html, 'html.parser')
        title = data.select_one("title").get_text()
        body = "".join(map(str, soup.select("article > div")))

        published_datetime = datetime.datetime\
            .strptime(data.select_one("pubDate").get_text(), "%a, %d %b %Y %H:%M:%S %Z")\
            .replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
        return {
            'title': title,
            'body': body,
            'published_datetime': published_datetime,
            'attachment_list': []
        }

    def site_id_from_data(self, data: Tag):
        data = urlparse(data.select_one('guid').get_text())
        return data.path

    def get_listing_url(self):
        return self.url

    def url_from_data(self, data: Tag):
        return data.select_one('guid').get_text(strip=True)