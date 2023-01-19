from unittest import TestCase


from crawler.IamCrawler import IamCrawler


class IamCrawlerTest(TestCase):
    def test_get_api_url(self):
        # given
        crawler = IamCrawler(url="https://school.iamservice.net/organization/19710/group/2091428")

        # when
        url = crawler._get_api_url()

        # then
        self.assertEqual(url, "https://school.iamservice.net/api/article/organization/19710/group/2091428")