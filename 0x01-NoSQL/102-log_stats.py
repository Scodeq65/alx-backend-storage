#!/usr/bin/env python3
""" Py script that provides stats about Nginx logs stored in MongoDB. """

from pymongo import MongoClient

def log_stats():
    """Function to display statistics about Nginx logs."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Total logs count
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # Methods statistics
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Status check for method GET and path /status
    status_check = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

    # Top 10 most present IPs
    print("IPs:")
    top_ips = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()

