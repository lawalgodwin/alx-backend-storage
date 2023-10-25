#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker

In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:).

The core of the function is very simple.

It uses the requests module to obtain the HTML content
of a particular URL and returns it.

Start in a new file named web.py and do not reuse the
code written in exercise.py.

Inside get_page track how many times a particular
URL was accessed in the key "count:{url}" and cache
the result with an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate a
slow response and test your caching.

Bonus: implement this use case with decorators."""

import redis
import requests
from typing import Callable
from functools import wraps

cache = redis.Redis()


def addwebcacheandtracker(func: Callable) -> Callable:
    """a get_page(crawler) decorator that adds caching to the crawller"""

    @wraps(func)
    def wrapper(url) -> str:
        """The decorated function wrapper"""
        url_access_count = f"count:{url}"
        cached_page_key = f'cached:{url}'
        cached_page = cache.get(cached_page_key)
        # get cached content
        if cached_page:
            return cached_page.decode("utf-8")
        # get content from database if not cached
        html_page_content = func(url)
        cache.incr(url_access_count)
        cache.setex(cached_page_key, 10, str(html_page_content))
        return html_page_content
    return wrapper


@addwebcacheandtracker
def get_page(url: str) -> str:
    """ Craw a web page and return the web page"""

    res = requests.get(url).text

    return (res)


if __name__ == '__main__':
    url = 'http://slowwly.robertomurray.co.uk'
    # url = 'http://google.com'
    result = get_page(url)
    print(result)
