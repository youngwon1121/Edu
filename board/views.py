import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from board.models import Post, Attachment
from crawlers.crawler import crawler_factory


@csrf_exempt
def get(request):
    if request.method == "POST":
        data = json.loads(request.body)

        parsed_data = get_post(data['url'])

        for data in parsed_data:
            post = Post(url=data['url'],
                        title=data['title'],
                        body=data['body'],
                        published_datetime=data['published_datetime'],
                        site=data['site'],
                        site_id=data['site_id']
                        )
            post.save()

            for attachment in data['attachment_list']:
                att = Attachment(file_name=attachment, post=post)
                att.save()

        return HttpResponse(parsed_data)


def get_post(url):
    crawler = crawler_factory(url)

    site_ids: dict = crawler.get_target_site_ids()

    duplicate_posts = duplicate_check(crawler.site, site_ids.keys())

    for post in duplicate_posts.values('site_id'):
        if post['site_id'] in site_ids:
            del site_ids[post['site_id']]

    return crawler.get_post(site_ids)


def duplicate_check(site, site_ids):
    return Post.objects.filter(site=site,
                               site_id__in=site_ids)
