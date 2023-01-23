from urllib.parse import urlparse

from crawlers.BBCCrawler import BBCCrawler
from crawlers.IamCrawler import IamCrawler
from crawlers.NaverBlogCrawler import NaverBlogCrawler
from crawlers.exceptions import UnsupportedURL


def crawler_factory(url):
    if "school.iamservice.net" in url:
        return IamCrawler(url)
    elif "blog.naver.com" in url:
        return NaverBlogCrawler(url)
    elif "feeds.bbci.co.uk" in url:
        return BBCCrawler(url)
    else:
        raise UnsupportedURL(url)

