#!/usr/bin/env python3

"""Improve 12-log_stats.py by adding the top 10 of the most
present IPs in the collection nginx of the database logs

The IPs top must be sorted
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
    print("IPs:")

    IP_pipeline = [
        {"$match": {}},
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    cursor = mongo_collection.aggregate(IP_pipeline)

    for doc in cursor:
        print(f"\t{doc['_id']}: {doc['count']}")


if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    print(f"{collection.count_documents({})} logs")
    print("Methods:")
    analyse_logs(collection)
