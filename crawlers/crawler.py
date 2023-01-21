from urllib.parse import urlparse

from crawlers.BBCCrawler import BBCCrawler
from crawlers.IamCrawler import IamCrawler
from crawlers.NaverBlogCrawler import NaverBlogCrawler


def crawler_factory(url):
    parts = urlparse(url)
    if parts.netloc == "school.iamservice.net":
        return IamCrawler(url)
    elif parts.netloc == "blog.naver.com":
        return NaverBlogCrawler(url)
    elif parts.netloc == "feeds.bbci.co.uk":
        return BBCCrawler(url)
    else:
        return None

