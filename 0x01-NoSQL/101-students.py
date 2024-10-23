#!/usr/bin/env python3
""" Py script that returns students sorted by average score. """

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Args:
        mongo_collection: the pymongo collection object.
        
    Returns:
        A list of students, each with the averageScore key.
    """
    return mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": { "$avg": "$topics.score" }
            }
        },
        { "$sort": { "averageScore": -1 } }
    ])

