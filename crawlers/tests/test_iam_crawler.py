import os

from django.test import TestCase

from crawlers.IamCrawler import IamCrawler
import json


class IamCrawlerTest(TestCase):
    def setUp(self) -> None:
        self.path = os.path.dirname(__file__)
        self.crawler = IamCrawler(url="https://school.iamservice.net/organization/19710/group/2091428")
        self.data = open(self.path + "/resources/iam.json").read()
        self.html = open(self.path + "/resources/iam.html").read()

    def test_get_listing_url(self):
        # when
        url = self.crawler.get_listing_url()

        # then
        self.assertEqual(url, "https://school.iamservice.net/api/article/organization/19710/group/2091428")

    def test_parse_index(self):
        #given
        data = json.loads(self.data)

        #when
        articles = self.crawler._parse_index(self.data)

        #then
        self.assertListEqual(data['articles'][:10], articles)


    def test_parse_post(self):
        # given
        json_data = json.loads(self.data)

        # when
        post = self.crawler._parse_post(self.html, json_data['articles'][0])

        # then
        self.assertTrue(post['body'].startswith("["))
        self.assertTrue(post['body'].endswith("]"))