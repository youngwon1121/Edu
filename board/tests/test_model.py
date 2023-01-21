import datetime
import zoneinfo

from django.test import TestCase

from board.models import Site, Post, Attachment
from django.utils import timezone

from board.views import duplicate_check


class MyTestCase(TestCase):
    def test_create(self):
        # given, when
        p = Post(
            url="https://school.iamservice.net/organization/1674/group/2001892",
            title="2023학년도 교과서 목록",
            body="aa👏",
            published_datetime=timezone.now(),
            site=Site.IAM
        )
        p.save()

        a1 = Attachment(file_name="경기도교육청 융합교육정책과_경기학교예술창작소 내안의 예술1(웹포스터).jpg", post=p)
        a2 = Attachment(file_name="경기도교육청 융합교육정책과_2023년 경기학교예술창작소 융합형 교육프로그램(발송용).hwp", post=p)
        a1.save()
        a2.save()

        # then
        p = Post.objects.get(id=1)
        self.assertEqual(p.id, 1)
        self.assertEqual(p.site, Site.IAM)
        self.assertEqual(p.attachment_set.count(), 2)

    def test_timezone2(self):
        bbc_time = "2023-01-18T14:00:28.000Z"
        t = timezone.datetime.strptime(bbc_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        print(t)

        iam_time = "2023-01-11 00:00:00"
        t = timezone.datetime.strptime(iam_time, '%Y-%m-%d %H:%M:%S')
        print(t)
        t = t.replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
        print(timezone.is_aware(t))

        naver_time = "2022. 11. 13. 10:00"
        t = timezone.datetime.strptime(naver_time, '%Y. %m. %d. %H:%M')
        print(t)

        # from django.utils.dateparse import parse_datetime
        # parse_datetime("2023-01-18T14:00:28.000Z")

    def test_timezone(self):
        import pytz
        from django.utils.dateparse import parse_date

        # naive
        repay_datetime = datetime.datetime.strptime('2016-10-01 14:00:00', '%Y-%m-%d %H:%M:%S')
        print(repay_datetime)

        # aware
        repay_aware_datetime = timezone.make_aware(repay_datetime)
        print(repay_aware_datetime)

        print('-----')
        now = timezone.now()
        print(timezone.localtime(timezone.now()))

        import NHNEdu.settings
        t_from = '20220801000000'
        from_dt = datetime.datetime(year=int(t_from[:4]), month=int(t_from[4:6]), day=int(t_from[6:8]),
                                    hour=int(t_from[8:10]),
                                    minute=int(t_from[10:12]), second=int(t_from[12:14]))
        print(from_dt)

    def test_duplicate_check(self):
        p1 = Post(
            url="https://school.iamservice.net/organization/1674/group/2001892",
            title="IAM1",
            body="aa👏",
            published_datetime=timezone.now(),
            site=Site.IAM,
            site_id="1234"
        )
        p1.save()
        p2 = Post(
            url="https://school.iamservice.net/organization/1674/group/2001892",
            title="BBC1",
            body="aa👏",
            published_datetime=timezone.now(),
            site=Site.IAM,
            site_id="5678"
        )
        p2.save()

        # 중복되는 id
        result_set = duplicate_check(Site.IAM, ["1234", "2345", "3456", "4567", "5678"])
        self.assertQuerysetEqual(result_set, [p1, p2], ordered=False)
