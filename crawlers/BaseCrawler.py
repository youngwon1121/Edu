from abc import ABCMeta, abstractmethod

import requests


class BaseCrawler(metaclass=ABCMeta):
    @abstractmethod
    def get_posts(self, url=None):
        pass

    @abstractmethod
    def get_target_site_ids(self):
        pass


class HtmlCrawler(BaseCrawler, metaclass=ABCMeta):
    def __init__(self, url):
        self.url = url
        self.site = None

    def get_posts(self, urls: dict = None):
        if urls is None:
            urls = self._get_urls()
            return [self.get_posts(url) for url in urls]

        return [self._get_post(url) for url in urls.values()]

    def get_target_site_ids(self):
        site_ids = dict()
        for url in self._get_urls():
            site_ids[self.to_site_id(url)] = url
        return site_ids

    def _get_urls(self):
        response = requests.get(self.url)
        return self._parse_index(response.content)

    def _get_post(self, url):
        response = requests.get(url).content
        data = self._parse_post(response)
        data['url'] = url
        data['site_id'] = self.to_site_id(url)
        data['site'] = self.site
        return data
    @abstractmethod
    def _parse_index(self, html):
        pass

    @abstractmethod
    def _parse_post(self, html):
        pass

    @abstractmethod
    def to_site_id(self, url):
        pass
