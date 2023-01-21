import re
import zoneinfo
from datetime import timedelta
from urllib.parse import urlparse, parse_qsl

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from crawlers.BaseCrawler import BaseCrawler


class NaverBlogCrawler(BaseCrawler):
    def __init__(self, url):
        self.url = url
        self.site = "NAVERBLOG"

    def get_post(self, urls: dict = None):
        if urls is None:
            urls = self._get_links()
        return self._get_details(urls.values())

    def get_target_site_ids(self) -> dict:
        site_ids = dict()
        for url in self._get_links():
            site_ids[self.to_site_id(url)] = url
        return site_ids

    def _get_links(self):
        response = requests.get(self.url).content
        return self._parse_index(response)

    def _parse_index(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return ['https://blog.naver.com' + item['href'] for item in soup.select('.item .link')[:10]]

    def _get_details(self, urls):
        data = []
        for url in urls:
            response = requests.get(url).content
            parsed_data = self._parse_detail(response)
            parsed_data['url'] = url
            parsed_data['site_id'] = self.to_site_id(url)
            parsed_data['site'] = self.site
            data.append(parsed_data)
        return data

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

    def _parse_datetime(self, dt):
        if r := re.search(r'(\d+)(?=분 전)', dt):
            return timezone.now() - timedelta(minutes=int(r.group()))

        elif r := re.search(r'(\d+)(?=시간 전)', dt):
            return timezone.now() - timedelta(hours=int(r.group()))

        else:
            return timezone.datetime.strptime(dt, '%Y. %m. %d. %H:%M').replace(tzinfo=zoneinfo.ZoneInfo("Asia/Seoul"))

    def to_site_id(self, url):
        """
        url로 부터 unique한 siteid 생성
        """
        url = urlparse(url)
        query = dict(parse_qsl(url.query))
        return 'blogId=' + str(query.get('blogId')) + "&" + 'logNo=' + str(query.get('logNo'))
