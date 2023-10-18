#!/usr/bin/env python3
"""A modile containing a function that lists all documents in a collection"""
from typing import Mapping, Any, List
from pymongo.collection import Collection


def list_all(mongo_collection: Collection) -> List[Mapping[str, Any]]:
    """ Retue a list of all documents in the given collection"""
    return [ doc for doc in mongo_collection.find({})]
