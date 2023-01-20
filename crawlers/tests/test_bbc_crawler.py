import os

from django.test import TestCase
from zoneinfo import ZoneInfo

from django.utils import timezone

from crawlers.BBCCrawler import BBCCrawler


class BBCCrawlerTest(TestCase):
    def setUp(self) -> None:
        self.path = os.path.dirname(__file__)

    def test_parse_index(self):
        # given
        crawler = BBCCrawler('http://feeds.bbci.co.uk/news/rss.xml')
        xml = open(self.path + "/resources/bbc.xml").read()

        # when
        urls = crawler._parse_index(xml)

        # then
        self.assertEqual(urls, ['https://www.bbc.co.uk/news/world-europe-64315594?at_medium=RSS&at_campaign=KARANGA',
                                'https://www.bbc.co.uk/news/uk-64304500?at_medium=RSS&at_campaign=KARANGA',
                                'https://www.bbc.co.uk/news/uk-64319133?at_medium=RSS&at_campaign=KARANGA',
                                'https://www.bbc.co.uk/news/uk-64315384?at_medium=RSS&at_campaign=KARANGA',
                                'https://www.bbc.co.uk/news/world-europe-64314673?at_medium=RSS&at_campaign=KARANGA',
                                'https://www.bbc.co.uk/news/health-64308935?at_medium=RSS&at_campaign=KARANGA',
                                'https://www.bbc.co.uk/news/business-64315925?at_medium=RSS&at_campaign=KARANGA',
                                'https://www.bbc.co.uk/news/uk-england-hereford-worcester-64235272?at_medium=RSS&at_campaign=KARANGA',
                                'https://www.bbc.co.uk/news/uk-politics-64318141?at_medium=RSS&at_campaign=KARANGA',
                                'https://www.bbc.co.uk/news/uk-wales-64317360?at_medium=RSS&at_campaign=KARANGA'])

    def test_parse_detail(self):
        # given
        crawler = BBCCrawler('http://feeds.bbci.co.uk/news/rss.xml')
        xml = open(self.path + "/resources/bbc_detail.html").read()

        # when
        data = crawler._parse_detail(xml)

        #then
        self.assertEqual(data['title'], "Ukraine's interior ministry leadership killed in helicopter crash")
        self.assertEqual(data['published_datetime'].tzinfo, ZoneInfo('UTC'))
        self.assertTrue(timezone.is_aware(data['published_datetime']))
