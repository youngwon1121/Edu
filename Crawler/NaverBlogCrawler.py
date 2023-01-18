import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class NaverBlogCrawler:
    def __init__(self, url):
        self.url = url
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        self.driver = webdriver.Chrome("../chromedriver", chrome_options=options)

    def get(self):
        urls = self._get_links()
        return self._get_details(urls)

    def _get_links(self):
        response = requests.get(url=self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return ['https://blog.naver.com/'+item['href'] for item in soup.find_all("a", class_="link pcol2")[:10]]

    def _get_details(self, urls):
        data = []
        for url in urls:
            self.driver.get(url)
            title = self.driver.find_element(by=By.CSS_SELECTOR, value=".se-title-text span").text
            body = self.driver.find_element(by=By.CLASS_NAME, value="se-main-container").get_attribute('innerHTML')
            published_datetime = self.driver.find_element(by=By.CLASS_NAME, value="se_publishDate").text
            attachment_list = [item.text for item in self.driver.find_elements(by=By.CLASS_NAME, value="se-file-name-container")]

            data.append({
                'url': url,
                'title': title,
                'body': body,
                'published_datetime': published_datetime,
                'attachment_list': attachment_list
            })
        return data

