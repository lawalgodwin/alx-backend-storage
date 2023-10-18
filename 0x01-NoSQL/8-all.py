#!/usr/bin/env python3
"""A modile containing a function that lists all documents in a collection"""
from typing import Mapping, Any, List, TypeVar
from pymongo.collection import Collection

T = TypeVar("T")


def list_all(mongo_collection: Collection) -> List[Mapping[str, Any]]:
    """ Retue a list of all documents in the given collection"""
    return list(mongo_collection.find({}))
