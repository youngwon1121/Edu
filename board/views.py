from django.http import HttpResponse
from django.shortcuts import render

import Crawler.crawler
from Crawler.crawler import get_post


def get(request):
    url = request.GET['url']

    data = get_post(url)

    return HttpResponse(data)