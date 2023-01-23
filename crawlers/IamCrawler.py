import zoneinfo
from urllib.parse import urlparse

import requests
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from crawlers.BaseCrawler import BaseCrawler


class IamCrawler(BaseCrawler):

    def __init__(self, url=None):
        super().__init__(url)
        self.site = "IAM"
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get_posts(self):
        posts = []
        for article in self.request_data.values():
            posts.append(self._get_post(article))
        return posts

    def refresh_request_data(self):
        json = self._get_json()
        for article in json['articles'][:10]:
            self.request_data[str(article['id'])] = article

    def _get_json(self):
        self.json = requests.get(self._get_api_url()).json()
        return self.json

    def _get_api_url(self):
        url = urlparse(self.url)
        return url._replace(path='/api/article' + url.path).geturl()

    def _get_post(self, article: dict):
        url = article['view_link']
        self.driver.get(url)
        body = self.driver.find_element(by=By.ID, value="articleBody").get_attribute('innerHTML')
        published_datetime = timezone.datetime.strptime(article['reg_date'], '%Y-%m-%d %H:%M:%S').replace(
            tzinfo=zoneinfo.ZoneInfo("Asia/Seoul"))

        file = []
        if article['files'] is not None:
            file = [file['title'] for file in article['files']]
        return {
            'url': url,
            'site': self.site,
            'site_id': article['id'],
            'title': article['title'],
            'body': body,
            'published_datetime': published_datetime,
            'attachment_list': file
        }
