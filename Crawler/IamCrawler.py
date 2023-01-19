from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class IamCrawler:
    def __init__(self, url):
        self.url = url
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
                'title': article['title'],
                'body': body,
                'published_datetime': article['pub_date'],
                'attachment_list': [file['title'] for file in article['files']]
            })
        return data





    # def _get_links(self):
    #     self.driver.get(self.url)
    #     return [e.get_attribute('href') for e in self.driver.find_elements(by=By.CLASS_NAME, value="btn_detail")[:10]]

    # def _get_details(self, urls):
    #     for url in urls:
    #         self.driver.get(url)
    #
    #         title = self.driver.find_element(by=By.CLASS_NAME, value="title").text
    #         body = self.driver.find_element(by=By.ID, value="articleBody").get_attribute('innerHtml')
    #         attachment_list = [e.find_element(By.TAG_NAME, "a").text
    #                            for e in self.driver.find_elements(by=By.CLASS_NAME, value="file-anchor")]




