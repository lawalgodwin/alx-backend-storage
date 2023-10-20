#!/usr/bin/env python3

"""Write a Python script that provides some stats about Nginx logs
stored in MongoDB:

Requirements:
    - Database: logs
    - Collection: nginx
    - Display (same as the example):
    - first line: x logs where x is the number of documents in this collection
    - second line: Methods:
    - 5 lines with the number of documents with the method =
        ["GET", "POST", "PUT", "PATCH", "DELETE"]
    - one line with the number of documents with:
        method=GET
        path=/status
"""
from pymongo.collection import Collection


def analyse_logs(mongo_collection: Collection) -> None:
    """Analyse nginx logs stored in the database"""
    cursor = mongo_collection.aggregate([
        {"$match": {}},
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ])

    allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    data = [{'method': doc.get("_id"), 'count': doc.get('count')}
            for doc in cursor
            ]

    fetched_methods = [doc.get('method') for doc in data]

    for method in allowed_methods:
        if method in fetched_methods:
            for doc in data:
                if (doc.get('method') == method):
                    print(f"\tmethod {method}: {doc.get('count')}")
        else:
            print(f"\tmethod {method}: 0")

    status_req_count = (mongo_collection.count_documents({'method': 'GET',
                                                          'path': '/status'}))
    print(f"{status_req_count} status check")


if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    print(f"{collection.count_documents({})} logs")
    analyse_logs(collection)
