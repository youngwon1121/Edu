import datetime
import os

from bs4 import BeautifulSoup
from django.test import TestCase
from zoneinfo import ZoneInfo

from django.utils import timezone

from crawlers.BBCCrawler import BBCCrawler


class BBCCrawlerTest(TestCase):
    def setUp(self) -> None:
        self.path = os.path.dirname(__file__)
        self.crawler = BBCCrawler('http://feeds.bbci.co.uk/news/rss.xml')
        self.xml = open(self.path + "/resources/bbc.xml").read()
        self.html = open(self.path + "/resources/bbc_detail.html").read()

    def test_parse_index(self):
        # when
        data = self.crawler._parse_index(self.xml)
        # then
        self.assertEqual(10, len(data))
        self.assertTrue(str(data[0]).startswith('<item>'))
        self.assertTrue(str(data[0]).endswith('</item>'))

    def test_parse_post(self):
        # given
        soup = BeautifulSoup(self.xml, 'xml')
        data = soup.select_one("item")

        # when
        data = self.crawler._parse_post(self.html, data)

        # then
        self.assertEqual(data['title'], "Ukraine interior ministry leadership killed in helicopter crash")
        self.assertEqual(data['published_datetime'].tzinfo, ZoneInfo('UTC'))
        self.assertTrue(timezone.is_aware(data['published_datetime']))

    def test_site_id_from_data(self):
        #given
        soup = BeautifulSoup(self.xml, 'xml')
        data = soup.select_one("item")

        #when, then
        self.assertEqual('/news/world-europe-64315594', self.crawler.site_id_from_data(data))


