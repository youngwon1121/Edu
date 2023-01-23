import os
from unittest.mock import patch, MagicMock, Mock
from zoneinfo import ZoneInfo

from django.test import TestCase
from django.utils import timezone

from crawlers.IamCrawler import IamCrawler
import json


class IamCrawlerTest(TestCase):
    def setUp(self) -> None:
        self.path = os.path.dirname(__file__)
        self.crawler = IamCrawler(url="https://school.iamservice.net/organization/19710/group/2091428")

    def test_get_api_url(self):
        # when
        url = self.crawler._get_api_url()

        # then
        self.assertEqual(url, "https://school.iamservice.net/api/article/organization/19710/group/2091428")

    def test_get_post(self):
        # given
        mock = Mock()
        mock.get.return_value = 'mock_get'
        mock.find_element().get_attribute.return_value = ''
        self.crawler.driver = mock
        data = open(self.path + "/resources/iam.json").read()
        response = json.loads(data)

        # when
        post = self.crawler._get_post(response['articles'][0])

        # then
        self.assertEqual("2023학년도 교과서 목록", post['title'])
        self.assertEqual(ZoneInfo('Asia/Seoul'), post['published_datetime'].tzinfo)
        self.assertTrue(timezone.is_aware(post['published_datetime']))
        self.assertListEqual(["2023학년도 교과서목록.xls"], post['attachment_list'])
        self.assertEqual(135964035, post['site_id'])