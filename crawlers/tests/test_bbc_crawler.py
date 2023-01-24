import datetime
import os

from django.test import TestCase
from zoneinfo import ZoneInfo

from django.utils import timezone

from crawlers.BBCCrawler import BBCCrawler


class BBCCrawlerTest(TestCase):
    def setUp(self) -> None:
        self.path = os.path.dirname(__file__)
        self.crawler = BBCCrawler('http://feeds.bbci.co.uk/news/rss.xml')

    def test_parse_index(self):
        # given
        xml = open(self.path + "/resources/bbc.xml").read()

        # when
        urls = self.crawler._parse_index(xml)
        # then
        self.assertEqual(urls, ['https://www.bbc.co.uk/news/business-64315925',
                                'https://www.bbc.co.uk/news/uk-64319133',
                                'https://www.bbc.co.uk/news/uk-england-hereford-worcester-64235272',
                                'https://www.bbc.co.uk/news/health-64308935',
                                'https://www.bbc.co.uk/news/uk-wales-64317360',
                                'https://www.bbc.co.uk/news/world-europe-64315594',
                                'https://www.bbc.co.uk/news/uk-64315384',
                                'https://www.bbc.co.uk/news/uk-politics-64318141',
                                'https://www.bbc.co.uk/news/uk-64304500',
                                'https://www.bbc.co.uk/news/business-55992592'])

    def test_parse_post(self):
        # given
        xml = open(self.path + "/resources/bbc_detail.html").read()

        # when
        data = self.crawler._parse_post(xml)

        # then
        self.assertEqual(data['title'], "Ukraine's interior ministry leadership killed in helicopter crash")
        self.assertEqual(data['published_datetime'].tzinfo, ZoneInfo('UTC'))
        self.assertTrue(timezone.is_aware(data['published_datetime']))

    def test_to_site_id(self):
        #given
        url = 'https://www.bbc.co.uk/news/health-64354661?at_medium=RSS&at_campaign=KARANGA'

        #when, then
        self.assertEqual('/news/health-64354661', self.crawler.to_site_id(url))

    def test_get_request_id(self):
        ids = self.crawler.get_request_ids()

        self.crawler.remove_request_data_by_id(ids[0])
        self.assertEqual(9, len(self.crawler.get_request_ids()))

