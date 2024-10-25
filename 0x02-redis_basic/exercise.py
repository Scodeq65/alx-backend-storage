#!/usr/bin/env python3
"""
Cache module for storing and retrieving data in Redis with random keys and counting method calls.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.
    
    Parameters:
    - method (Callable): The method to be decorated.
    
    Returns:
    - Callable: The wrapped method with call counting.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Use the qualified name of the method as the key for counting
        key = method.__qualname__
        # Increment the count for this key in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    
    return wrapper

class Cache:
    """Cache class for storing data with unique keys in Redis."""

    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return a randomly generated key.

        Parameters:
        - data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
        - str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis by key and optionally convert it using a callable.

        Parameters:
        - key (str): The key under which the data is stored.
        - fn (Optional[Callable]): A callable function to convert data.

        Returns:
        - Optional[Union[str, bytes, int, float]]: The retrieved data, converted if fn is provided.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data as a UTF-8 string.

        Parameters:
        - key (str): The key under which the data is stored.

        Returns:
        - Optional[str]: The retrieved data as a string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data as an integer.

        Parameters:
        - key (str): The key under which the data is stored.

        Returns:
        - Optional[int]: The retrieved data as an integer.
        """
        return self.get(key, fn=int)
