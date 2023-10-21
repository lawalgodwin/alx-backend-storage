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


def analyse_logs(mongo_collection):
    """Analyse nginx logs stored in the database"""
    allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in allowed_methods:
        request_count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {request_count}")

    status_req_count = (mongo_collection.count_documents({'method': 'GET',
                                                          'path': '/status'}))
    print(f"{status_req_count} status check")


if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    print(f"{collection.count_documents({})} logs")
    print("Methods:")
    analyse_logs(collection)
