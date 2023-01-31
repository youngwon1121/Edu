from board.models import Post, Attachment, PostSequence
from crawlers.crawler import crawler_factory
import hashlib

def get_post(url):
    crawler = crawler_factory(url)

    crawler.refresh_request_data()

    # 새 post 가져오기
    posts = crawler.get_posts()

    # 저장
    post_sequence = PostSequence.objects.create()
    post_list = []
    attachments_list = []

    # hash값으로 중복검색
    for post in posts:
        post['hash_content'] = hashlib.md5((post['title']+post['body']).encode('utf-8')).hexdigest()
    hashed_bodies = [post['hash_content'] for post in posts]
    duplicated_hash = Post.objects.filter(hash_content__in=hashed_bodies).values_list('hash_content', flat=True)

    #중복 데이터 처리
    for post in posts:
        if post['hash_content'] in duplicated_hash:
            continue
        p = Post(url=post['url'],
                 title=post['title'],
                 body=post['body'],
                 published_datetime=post['published_datetime'],
                 hash_content=post['hash_content'],
                 site=post['site'],
                 sequence=post_sequence
                 )
        post_list.append(p)

        for attachment in post['attachment_list']:
            att = Attachment(file_name=attachment, post=p)
            attachments_list.append(att)


    Post.objects.bulk_create(post_list)
    Attachment.objects.bulk_create(attachments_list)

    return Post.objects.prefetch_related('attachment_list')\
        .filter(sequence=post_sequence)\
        .order_by('-published_datetime')
