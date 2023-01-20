import os

from django.test import TestCase


from crawlers.IamCrawler import IamCrawler


class IamCrawlerTest(TestCase):
    def setUp(self) -> None:
        self.path = os.path.dirname(__file__)

    def test_get_api_url(self):
        # given
        crawler = IamCrawler(url="https://school.iamservice.net/organization/19710/group/2091428")

        # when
        url = crawler._get_api_url()

        # then
        self.assertEqual(url, "https://school.iamservice.net/api/article/organization/19710/group/2091428")