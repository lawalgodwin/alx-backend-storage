#!/usr/bin/env python3
"""A module that with a function for inserting a doc into collection"""
from pymongo.collection import Collection


def insert_school(mongo_collection: Collection, **kwargs):
    """Insert doc into the given collection and return the id"""
    return mongo_collection.insert_one(kwargs).inserted_id
