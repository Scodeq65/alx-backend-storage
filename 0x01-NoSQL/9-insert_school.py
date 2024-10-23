#!/usr/bin/env python3
""" Py script that insert a new doc in a collectiion
based on kwargs.
"""
def insert_school(mongo_collection, **kwargs):
    """
    insert a new document in a collection based on kwargs.

    Args:
        Mongo_collection: the ptmongo collection object.
        **kwargs: arbituary keyword arguments representing
        the document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
