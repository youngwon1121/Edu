import json

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from board.models import Post, Attachment
from board.serailizers import PostSerializer
from crawlers.crawler import crawler_factory


@csrf_exempt
@transaction.atomic
def get(request):
    if request.method == "POST":
        data = json.loads(request.body)

        posts = get_post(data['url'])
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)


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
