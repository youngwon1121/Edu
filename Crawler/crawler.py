from typing import Optional
from urllib.parse import urlparse

from Crawler.BBCCrawler import BBCCrawler
from Crawler.IamCrawler import IamCrawler
from Crawler.NaverBlogCrawler import NaverBlogCrawler


def crawler_factory(url):
    parts = urlparse(url)
    if parts.netloc == "school.iamservice.net":
        return IamCrawler
    elif parts.netloc == "blog.naver.com":
        return NaverBlogCrawler
    elif parts.netloc == "feeds.bbci.co.uk":
        return BBCCrawler
    else:
        return None


def get_post(url):
    crawler = crawler_factory(url)
    return crawler(url=url).get()

