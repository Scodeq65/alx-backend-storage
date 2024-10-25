#!/usr/bin/env python3
"""
Web caching and access counting module
"""

import requests
import redis
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator to count the number of requests to a specific URL."""
    @wraps(method)
    def wrapper(url: str) -> str:
        # Increment the count for the URL
        redis_client.incr(f"count:{url}")
        return method(url)
    return wrapper


def cache_result(expiration: int = 10) -> Callable:
    """Decorator to cache the result of a
    function for a set expiration time.
    """
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            # Check if the result is cached
            cached_result = redis_client.get(f"cache:{url}")
            if cached_result:
                return cached_result.decode("utf-8")

            # If not cached, fetch and cache the result
            result = method(url)
            redis_client.setex(f"cache:{url}", expiration, result)
            return result
        return wrapper
    return decorator


@count_requests
@cache_result(expiration=10)
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and return it as a string."""
    response = requests.get(url)
    return response.text
