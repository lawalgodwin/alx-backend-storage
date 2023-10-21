#!/usr/bin/env python3
"""A module containing the basic usage of redis database"""

import redis
from uuid import uuid4
from typing import Union


class Cache:
    def __init__(self):
        """Store an instance of the redis database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the given data in redis and returns the key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key
