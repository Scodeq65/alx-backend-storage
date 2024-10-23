#!/usr/bin/env python3
""" A py script that lists all documents in a collection."""


def list_all(mongo_collection):
    """
    List all documents in a collection
    """
    return list(mongo_collection.find())
