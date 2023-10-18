#!/usr/bin/env python3
"""A modile containing a function that lists all documents in a collection"""


def list_all(mongo_collection):
    """ Retue a list of all documents in the given collection"""
    return [ doc for doc in mongo_collection.find({})]
