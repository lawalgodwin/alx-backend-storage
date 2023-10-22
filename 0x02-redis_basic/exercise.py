#!/usr/bin/env python3


import redis
from uuid import uuid4
from typing import Union, Optional, Callable

"""Task 2: Incrementing values

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

Decorate Cache.store with count_calls
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

# Task 3: Storing List:
# Familiarize yourself with redis commands RPUSH, LPUSH, LRANGE, etc.

# In this task, we will define a call_history decorator to store the
# history of inputs and outputs for a particular function.
# Everytime the original function will be called, we will add its
# input parameters to one list in redis, and store its output into
# another list.
# In call_history, use the decorated function’s qualified name and
# append ":inputs" and ":outputs" to create input and output list keys
# respectively.
# call_history has a single parameter named method that is a Callable
# and returns a Callable.
# In the new function that the decorator will return, use rpush to
# append the input arguments. Remember that Redis can only store strings,
# bytes and numbers. Therefore, we can simply use str(args) to normalize.
# We can ignore potential kwargs for now.
# Execute the wrapped function to retrieve the output.
# Store the output using rpush in the "...:outputs" list,
# then return the output.
# Decorate Cache.store with call_history.


def call_history(method: Callable) -> Callable:
    """Decorator function for keeping track of input and output"""
    input_list = f'{method.__qualname__}:inputs'
    output_list = f'{method.__qualname__}:outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(input_list, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_list, output)
        return output
    return wrapper

# """Task 4: Retrieving lists
# In this tasks, we will implement a replay function to display the
# history of calls of a particular function.
# Use keys generated in previous tasks to generate the following output:
# >>> cache = Cache()
# >>> cache.store("foo")
# >>> cache.store("bar")
# >>> cache.store(42)
# >>> replay(cache.store)
# Cache.store was called 3 times:
# Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
# Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
# Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
# """


def replay(method: Callable) -> None:
    """Display the history of both input and output"""
    db = redis.Redis()
    input_list = f'{method.__qualname__}:inputs'
    output_list = f'{method.__qualname__}:outputs'
    function_name = method.__qualname__
    method_call_count = db.get(function_name)
    print("{} was called {} times:".format(function_name, method_call_count))
    for input, output in zip(input_list, output_list):
        try:
            input = input.decode('utf-8')
            output = output.decode('utf-8')
        except Exception:
            input = output = ""
        finally:
            print("{}(*{}) -> {}".format(function_name, input, output))


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
    @call_history
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
