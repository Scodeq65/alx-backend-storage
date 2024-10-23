#!/usr/bin/env python3
""" Provides some stats about Nginx logs stored in MongoDB. """

from pymongo import MongoClient


def log_stats():
    """ Function to print stats about Nginx logs in MongoDB """
    
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    
    # Connect to the logs database and nginx collection
    db = client.logs
    collection = db.nginx

    # Total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Number of logs for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")
    
    # Number of logs where method is GET and path is /status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    log_stats()

