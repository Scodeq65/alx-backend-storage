#!/usr/bin/env python3
"""
Cache module for storing data in Redis with random keys.
"""

import redis
import uuid
from typing import Union

class Cache:
    """Cache class for storing data with unique keys in Redis."""

    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
