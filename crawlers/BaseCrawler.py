from abc import ABCMeta, abstractmethod

import requests


class BaseCrawler(metaclass=ABCMeta):
    @abstractmethod
    def get_post(self, url=None):
        pass

    @abstractmethod
    def get_target_site_ids(self):
        pass


class HtmlCrawler(BaseCrawler, metaclass=ABCMeta):
    def __init__(self, url):
        self.url = url
        self.site = None

    def get_post(self, urls: dict = None):
        if urls is None:
            urls = self._get_links()
        return self._get_details(urls.values())

    def get_target_site_ids(self):
        site_ids = dict()
        for url in self._get_links():
            site_ids[self.to_site_id(url)] = url
        return site_ids

    def _get_links(self):
        response = requests.get(self.url)
        return self._parse_index(response.content)

    def _get_details(self, urls):
        data = []
        for url in urls:
            response = requests.get(url).content
            parse_data = self._parse_detail(response)
            parse_data['url'] = url
            parse_data['site_id'] = self.to_site_id(url)
            parse_data['site'] = self.site
            data.append(parse_data)
        return data

    @abstractmethod
    def _parse_index(self, html):
        pass

    @abstractmethod
    def _parse_detail(self, html):
        pass

    @abstractmethod
    def to_site_id(self, url):
        pass
