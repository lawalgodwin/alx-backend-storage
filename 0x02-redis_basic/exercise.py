#!/usr/bin/env python3
"""A module containing the basic usage of redis database"""

from redis import Redis
from uuid import uuid4
from typing import Union


class Cache:
    def __init__(self) -> Redis:
        """Constructor for the Cache class"""
        self.__redis = Redis()
        self.__redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the given data in redis and returns the key"""
        self.key = str(uuid4())
        self.__redis.set(self.key, data)
        return self.key