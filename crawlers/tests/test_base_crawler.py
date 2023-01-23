import os
from unittest.mock import patch

from django.test import TestCase

from crawlers.BaseCrawler import BaseCrawler


class BaseCrawlerTest(TestCase):

    def setUp(self) -> None:
        self.path = os.path.dirname(__file__)

    @patch("crawlers.BaseCrawler.BaseCrawler.__abstractmethods__", set())
    def test_get_request_id(self):
        # given
        crawler = BaseCrawler(url='')
        crawler.request_data['k1'] = 'key1'
        crawler.request_data['k2'] = 'key2'

        # when, then
        self.assertListEqual([
            'k1', 'k2'
        ], crawler.get_request_ids())

    @patch("crawlers.BaseCrawler.BaseCrawler.__abstractmethods__", set())
    def test_get_request_data(self):
        # given
        crawler = BaseCrawler(url='')
        crawler.request_data['k1'] = 'key1'
        crawler.request_data['k2'] = 'key2'

        # when, then
        self.assertListEqual([
            'key1', 'key2'
        ], crawler.get_request_datas())

    @patch("crawlers.BaseCrawler.BaseCrawler.__abstractmethods__", set())
    def test_remove_request_data_by_id(self):
        # given
        crawler = BaseCrawler(url='')
        crawler.request_data['k1'] = 'key1'
        crawler.request_data['k2'] = 'key2'

        # when
        crawler.remove_request_data_by_id('k1')

        # then
        self.assertListEqual([
            'k2'
        ], crawler.get_request_ids())



