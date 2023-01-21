import re
import zoneinfo
from datetime import timedelta
from urllib.parse import urlparse, parse_qsl

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from crawlers.BaseCrawler import HtmlCrawler


class NaverBlogCrawler(HtmlCrawler):
    def __init__(self, url):
        self.url = url
        self.site = "NAVERBLOG"

    def _parse_index(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return ['https://blog.naver.com' + item['href'] for item in soup.select('.item .link')[:10]]

    def _parse_detail(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select_one(".se-title-text span").get_text(strip=True)
        body = soup.find(class_="se-main-container")
        published_datetime = soup.find(class_="se_publishDate").get_text(strip=True)
        attachment_list = [item.get_text(strip=True) for item in soup.find_all(class_="se-file-name-container")]
        published_datetime = self._parse_datetime(published_datetime)
        return {
            'title': title,
            'body': str(body),
            'published_datetime': published_datetime,
            'attachment_list': attachment_list
        }

    def to_site_id(self, url):
        """
        url로 부터 unique한 siteid 생성
        """
        url = urlparse(url)
        query = dict(parse_qsl(url.query))
        return 'blogId=' + str(query.get('blogId')) + "&" + 'logNo=' + str(query.get('logNo'))

    def _parse_datetime(self, dt):
        if r := re.search(r'(\d+)(?=분 전)', dt):
            return timezone.now() - timedelta(minutes=int(r.group()))

        elif r := re.search(r'(\d+)(?=시간 전)', dt):
            return timezone.now() - timedelta(hours=int(r.group()))

        else:
            return timezone.datetime.strptime(dt, '%Y. %m. %d. %H:%M').replace(tzinfo=zoneinfo.ZoneInfo("Asia/Seoul"))
