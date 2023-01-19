import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class NaverBlogCrawler:
    def __init__(self, url):
        self.url = url
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get(self):
        urls = self._get_links()
        return self._get_details(urls)

    def _get_links(self):
        self.driver.get(url=self.url)
        # print(requests.get(url=self.url).content)
        return self._parse_index(self.driver.page_source)

    def _parse_index(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return ['https://blog.naver.com' + item['href'] for item in soup.find_all("a", class_="link pcol2")[:10]]

    def _get_details(self, urls):
        data = []
        for url in urls:
            self.driver.get(url)
            parsed_data = self._parse_detail(self.driver.page_source)
            parsed_data['url'] = url
            data.append(url)
        return data

    def _parse_detail(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select_one(".se-title-text span").get_text(strip=True)
        body = soup.find(class_="se-main-container")
        published_datetime = soup.find(class_="se_publishDate").get_text(strip=True)
        attachment_list = [item.get_text(strip=True) for item in soup.find_all(class_="se-file-name-container")]
        return {
            'title': title,
            'body': body,
            'published_datetime': published_datetime,
            'attachment_list': attachment_list
        }
