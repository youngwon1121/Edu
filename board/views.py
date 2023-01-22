from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from board.models import Post, Attachment
from board.serailizers import PostSerializer
from crawlers.crawler import crawler_factory


@api_view(['POST'])
@transaction.atomic
def get(request: Request):
    if request.method == "POST":
        if request.data.get('url') is None:
            return Response({"message": "Field 'url' is empty"}, status=status.HTTP_400_BAD_REQUEST)

        posts = get_post(request.data['url'])
        serializer = PostSerializer(posts, many=True)
        return Response(
            {'count': len(serializer.data), 'data': serializer.data},
            status=status.HTTP_200_OK
        )


def get_post(url):
    crawler = crawler_factory(url)

    request_ids = crawler.get_request_ids()

    # 중복 post 체크
    duplicate_posts = duplicate_check(crawler.site, request_ids)

    # 리스트 중 중복이 아닌것만 남기기
    for post in duplicate_posts.values('site_id'):
        crawler.remove_request_data_by_id(post['site_id'])

    # 새 post 가져오기
    posts = crawler.get_posts()

    # 저장
    for post in posts:
        p = Post(url=post['url'],
                 title=post['title'],
                 body=post['body'],
                 published_datetime=post['published_datetime'],
                 site=post['site'],
                 site_id=post['site_id']
                 )
        p.save()

        for attachment in post['attachment_list']:
            att = Attachment(file_name=attachment, post=p)
            att.save()

    return Post.objects.prefetch_related('attachment_list').filter(site=crawler.site, site_id__in=request_ids)


def duplicate_check(site, site_ids):
    return Post.objects.filter(site=site,
                               site_id__in=site_ids)
