#!/usr/bin/env python3
""" Function to update topics of a school document
based on the name.
"""


def update_topics(mongo_collection, name, topics):
    """ Update the topics of a school document.

    Args:
        mongo_collecion: The pymongo collection object.
        name (str): the school name to update.
        topics (list): A list of strings representing topics.
    """
    mongo_collection.update_one(
        {"name": name},
        {"$set": {"topics": topics}}
    )
