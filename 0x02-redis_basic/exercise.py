#!/usr/bin/env python3
"""A module containing the basic usage of redis database"""

import redis
from uuid import uuid4
from typing import Union


class Cache:
    def __init__(self) -> redis.Redis:
        """Store an instance of the redis database"""
        self.__redis = redis.Redis()
        self.__redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the given data in redis and returns the key"""
        key = str(uuid4())
        self.__redis.set(key, data)
        return key
