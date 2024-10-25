#!/usr/bin/env python3
"""
Cache module for storing and retrieving data in Redis with random keys,
tracking call count and storing call history of method inputs and outputs.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store history of function calls, including input parameters and output.
    
    Parameters:
    - method (Callable): The method to be decorated.
    
    Returns:
    - Callable: The wrapped method with call history tracking.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Generate Redis keys for inputs and outputs
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        # Log inputs to Redis
        self._redis.rpush(inputs_key, str(args))

        # Call the original method to get the output
        result = method(self, *args, **kwargs)

        # Log the output to Redis
        self._redis.rpush(outputs_key, str(result))

        return result

    return wrapper

class Cache:
    """Cache class for storing data with unique keys in Redis."""

    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Optional[Union[str, bytes, int, float]]:
        """Retrieve data from Redis by key and optionally convert it using a callable."""
        data = self._redis.get(key)
        return fn(data) if fn and data else data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve data as a UTF-8 string."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve data as an integer."""
        return self.get(key, fn=int)
