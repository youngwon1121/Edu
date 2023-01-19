import requests
from bs4 import BeautifulSoup

class BBCCrawler:
    def __init__(self, url):
        self.url = url
        self.site = "BBC"

    def get(self):
        urls = self._get_links()
        return self._get_details(urls)

    def _get_links(self):
        response = requests.get("http://feeds.bbci.co.uk/news/rss.xml")
        return self._parse_index(response.content)

    def _parse_index(self, xml):
        soup = BeautifulSoup(xml, "xml")
        return [link.get_text() for link in soup.select('item > link')[:10]]

    def _get_details(self, urls):
        data = []
        for url in urls:
            response = requests.get(url).content
            parse_data = self._parse_detail(response)
            parse_data['url'] = url
            parse_data['site'] = self.site
            data.append(parse_data)
        return data

    def _parse_detail(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find("h1", id="main-heading").get_text(strip=True)
        body = "".join(map(str, soup.select("article > div")))
        published_datetime = soup.select_one("header time")['datetime']
        return {
            'title': title,
            'body': body,
            'published_datetime': published_datetime,
            'attachment_list': []
        }