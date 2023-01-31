import asyncio
from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Dict, List

import requests

T = TypeVar("T")


class BaseCrawler(Generic[T], metaclass=ABCMeta):
    def __init__(self, url):
        self.site = None
        self.request_data: Dict[str, T] = {}
        self.url = url

    @abstractmethod
    def get_posts(self):
        pass

    @abstractmethod
    def refresh_request_data(self):
        pass

    def get_request_ids(self) -> List[str]:
        return list(self.request_data.keys())

    def get_request_datas(self) -> List[T]:
        return list(self.request_data.values())

    def remove_request_data_by_id(self, post_id: str):
        if post_id in self.request_data:
            del self.request_data[post_id]
            return True
        else:
            return False


class RequestCrawler(BaseCrawler[T], metaclass=ABCMeta):

    def __init__(self, url):
        super().__init__(url)

    def get_posts(self):
        return asyncio.run(self._get_posts_async())

    async def _get_posts_async(self):
        futures = [asyncio.ensure_future(self._fetch_post(data)) for data in self.request_data.values()]
        result = await asyncio.gather(*futures)
        return result

    def refresh_request_data(self):
        """
            {게시물 unique key: data}을 내부에 저장
        """
        for data in self._fetch_request_data():
            self.request_data[self.site_id_from_data(data)] = data

    def _fetch_request_data(self):
        """
            index페이지에서 게시물들의 URL을 가져온다
        """
        response = requests.get(self.get_listing_url())
        return self._parse_index(response.content)

    async def _fetch_post(self, data):
        """
            각각의 게시물을 가져온다
        """
        loop = asyncio.get_event_loop()
        url = self.url_from_data(data)
        response = await loop.run_in_executor(None, requests.get, url)
        post = self._parse_post(response.content, data)
        post['url'] = url
        post['site_id'] = self.site_id_from_data(data)
        post['site'] = self.site
        return post

    @abstractmethod
    def get_listing_url(self):
        pass

    @abstractmethod
    def _parse_index(self, html) -> List[T]:
        pass

    @abstractmethod
    def _parse_post(self, html, data):
        pass

    @abstractmethod
    def site_id_from_data(self, data) -> str:
        pass

    @abstractmethod
    def url_from_data(self, data):
        pass
