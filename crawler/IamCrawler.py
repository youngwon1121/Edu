from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class IamCrawler:
    def __init__(self, url):
        self.url = url
        self.site = "IAM"
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get(self):
        json = self._get_json()
        return self._get_details(json)

    def _get_json(self):
        return requests.get(self._get_api_url()).json()

    def _get_api_url(self):
        url = urlparse(self.url)
        return url._replace(path='/api/article'+url.path).geturl()

    def _get_details(self, json):
        data = []
        for article in json['articles'][:10]:
            url = article['view_link']

            self.driver.get(url)
            body = self.driver.find_element(by=By.ID, value="articleBody").get_attribute('innerHTML')

            data.append({
                'url': url,
                'site': self.site,
                'title': article['title'],
                'body': body,
                'published_datetime': article['pub_date'],
                'attachment_list': [file['title'] for file in article['files']]
            })
        return data
