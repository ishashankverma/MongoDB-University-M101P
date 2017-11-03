#!/usr/bin/env python
import pymongo

# It is not necessary to import sys

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")

# get a handle to the students database
db = connection.students
grades = db.grades

def find_ids():
    """
    Returns the IDs of the lowest homework score.
    """
    query = {'type': 'homework'}
    cursor = grades.find(query).sort([('student_id', pymongo.ASCENDING), ('score', pymongo.ASCENDING)])
    old_student_id = 1
    id_list = []
    i = 0
    for doc in cursor:
        student_id = doc['student_id']
        if student_id == old_student_id:
            continue
        id_list.append(doc['_id'])
        i = i + 1
        old_student_id = student_id
    return id_list


def delete(listed):
    """
    Delete the records with the recieved IDs
    Argument:
    listed -- the list of IDs to be deleted
    """
    count = 0
    for li in listed:
        result = grades.delete_one({'_id': li})
        count = count + result.deleted_count
    print(count)


if __name__ == '__main__':
    list_id = find_ids()
    print(len(list_id))
    delete(list_id)