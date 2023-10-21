#!/usr/bin/env python3


import redis
from uuid import uuid4
from typing import Union, Optional, Callable

"""Task 3: Incrementing values

Familiarize yourself with the INCR command and its python equivalent.

In this task, we will implement a system to count how many times methods
of the Cache class are called.

Above Cache define a count_calls decorator that takes a single method
Callable argument and returns a Callable.

As a key, use the qualified name of method using the
__qualname__ dunder method.

Create and return function that increments the count for that key

every time the method is called and returns the value returned by

the original method.

Remember that the first argument of the wrapped function will

be self which is the instance itself, which lets you access

the Redis instance.

Protip: when defining a decorator it is useful to use functool.wraps

to conserve the original function’s name, docstring, etc.

Make sure you use it as described here:
https://docs.python.org/3.7/library/functools.html#functools.wraps
"""
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """A decorator for a funtion that counts method calls on redis"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for the decorated function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


"""Task 0:  Writing strings to Redis

Create a Cache class. In the __init__ method, store an instance
of the Redis client as a private variable named _redis (using redis.Redis())
and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.

The method should generate a random key (e.g. using uuid), store the
input data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a

str, bytes, int or float
"""
UnionOfTypes = Union[str, bytes, int, float]


class Cache:
    def __init__(self):
        """Store an instance of the redis database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: UnionOfTypes) -> str:
        """Store the given data in redis and returns the key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    """Task 1: Reading from Redis and recovering original type.
    Redis only allows to store string, bytes and numbers
    (and lists thereof).
    Whatever you store as single elements, it will be returned as
    a byte string.
    Hence if you store "a" as a UTF-8 string, it will be returned as b"a"
    when retrieved from the server.

    In this exercise we will create a get method that take a
    key string argument
    and an optional Callable argument named fn. This callable will be used to
    convert the data back to the desired format.

    Remember to conserve the original Redis.get behavior if the key does
    not exist.

    Also, implement 2 new methods: get_str and get_int that will automatically
    parametrize Cache.get with the correct conversion function.
    """

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """Retreive value from cache using the key and return a handler
        for converting the retreived data to the desired state"""
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key):
        """get value in string value"""
        return self.get(key, str)

    def get_int(self, key):
        """get value in integer format"""
        return self.get(key, int)
