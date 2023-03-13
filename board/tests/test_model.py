from django.test import TestCase

from board.models import Site, Post, Attachment, PostSequence
from django.utils import timezone



class MyTestCase(TestCase):
    def setUp(self):
        self.sequence = PostSequence()
        self.sequence.save()
    def test_create(self):
        # given, when
        p = Post(
            url="https://school.iamservice.net/organization/1674/group/2001892",
            title="2023학년도 교과서 목록",
            body="aa👏",
            published_datetime=timezone.now(),
            site=Site.IAM,
            sequence=self.sequence
        )
        p.save()

        a1 = Attachment(file_name="경기도교육청 융합교육정책과_경기학교예술창작소 내안의 예술1(웹포스터).jpg", post=p)
        a2 = Attachment(file_name="경기도교육청 융합교육정책과_2023년 경기학교예술창작소 융합형 교육프로그램(발송용).hwp", post=p)
        a1.save()
        a2.save()

        # then
        self.assertEqual(p.id, 1)
        self.assertEqual(p.site, Site.IAM)
        self.assertEqual(p.attachment_list.count(), 2)

    def test_relation_name(self):
        # given
        p1 = Post(
            url="https://school.iamservice.net/organization/1674/group/2001892",
            title="IAM1",
            body="aa👏",
            published_datetime=timezone.now(),
            site=Site.IAM,
            sequence=self.sequence
        )
        p1.save()

        # when
        self.assertEqual(0, p1.attachment_list.all().count())

    def test_duplicate(self):
        p1 = Post(
            url="https://school.iamservice.net/organization/1674/group/2001892",
            title="IAM1",
            body="aa👏",
            published_datetime=timezone.now(),
            site=Site.IAM,
            hash_content='aaaaaa',
            sequence=self.sequence
        )
        p1.save()

        hash_content = Post.objects.filter(hash_content__in=['aaaaaa']).values_list('hash_content', flat=True)
        self.assertEqual('aaaaaa', hash_content[0])
# ./manage.py test