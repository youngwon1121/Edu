import datetime
import os

from django.test import TestCase
from zoneinfo import ZoneInfo

from django.utils import timezone

from crawlers.NaverBlogCrawler import NaverBlogCrawler


class NaverBlogCrawlerTest(TestCase):
    def setUp(self) -> None:
        self.path = os.path.dirname(__file__)
        self.crawler = NaverBlogCrawler("https://blog.naver.com/PostList.nhn?blogId=sntjdska123&from=postList&categoryNo=51")

    def test_get_listing_url(self):
        url = self.crawler.get_listing_url()
        self.assertEqual("https://blog.naver.com/PostTitleListAsync.naver?blogId=sntjdska123&from=postList&categoryNo=51&currentPage=1&countPerPage=10", url)

    def test_parse_index(self):
        # given
        json = open(self.path + "/resources/naverblog.json").read()

        # when
        urls = self.crawler._parse_index(json)
        # then
        self.assertEqual('https://blog.naver.com/PostView.nhn?blogId=sntjdska123&from=postList&categoryNo=51&logNo=222991430176',
                         urls[0])


    def test_parse_post(self):
        # given
        html = open(self.path + "/resources/naverblog_detail.html").read()

        # when
        data = self.crawler._parse_post(html)

        # then
        self.assertEqual(data['title'], "[첨부파일] 수소차 관련주 (2030년까지 수소차 3만대 보급 , 수소 경제 정책 방향) 대창솔루션 / 평화홀딩스 / 대원강업 / 세종공업 / 평화산업")
        self.assertListEqual(data['attachment_list'], [
            "221109(18시) 새정부 첫번째 수소경제위원회 개최, 수소산업 본격 성장을 위한 정책방향 제시(해양수산과학기술정책과).hwpx",
            "221109(18시) 새정부 첫번째 수소경제위원회 개최, 수소산업 본격 성장을 위한 정책방향 제시(해양수산과학기술정책과).pdf"
        ])
        self.assertTrue(str(data['body']).startswith('<div class="se-main-container">'))
        self.assertEqual(data['published_datetime'].tzinfo, ZoneInfo('Asia/Seoul'))
        self.assertTrue(timezone.is_aware(data['published_datetime']))



    def test_parse_time(self):
        # given
        times = ["5분 전", "58분 전", "1시간 전", "11시간 전"]

        #when
        for time in times:
            self.crawler._parse_datetime(time)

    def test_create_site_id(self):
        #given
        urls = [
            'https://blog.naver.com/PostView.naver?blogId=hellopolicy&logNo=222989752607&categoryNo=168&parentCategoryNo=&from=thumbnailList',
            'https://blog.naver.com/PostView.naver?blogId=hellopolicy&logNo=222930899202&categoryNo=168&parentCategoryNo=&from=thumbnailList']

        # when then
        self.assertEqual('blogId=hellopolicy&logNo=222989752607', self.crawler.to_site_id(urls[0]))