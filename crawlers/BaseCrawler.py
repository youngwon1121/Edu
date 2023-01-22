import asyncio
from abc import ABCMeta, abstractmethod

import requests


class BaseCrawler(metaclass=ABCMeta):
    def __init__(self, url):
        self.request_data = {}
        self.url = url
        self.refresh_request_data()

    @abstractmethod
    def get_posts(self):
        pass

    @abstractmethod
    def refresh_request_data(self):
        pass

    def get_request_ids(self):
        return list(self.request_data.keys())

    def get_request_datas(self):
        return list(self.request_data.values())

    def remove_request_data_by_id(self, post_id):
        if post_id in self.request_data:
            del self.request_data[post_id]
            return True
        else:
            return False


class HtmlCrawler(BaseCrawler, metaclass=ABCMeta):
    def __init__(self, url):
        super().__init__(url)
        self.site = None

    def get_posts(self):
        return asyncio.run(self._get_posts())

    async def _get_posts(self):
        futures = [asyncio.ensure_future(self._get_post(url)) for url in self.request_data.values()]
        result = await asyncio.gather(*futures)
        return result

    def refresh_request_data(self):
        for url in self._get_urls():
            self.request_data[self.to_site_id(url)] = url

    def _get_urls(self):
        response = requests.get(self.url)
        return self._parse_index(response.content)

    async def _get_post(self, url):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, requests.get, url)
        data = self._parse_post(response.content)
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
