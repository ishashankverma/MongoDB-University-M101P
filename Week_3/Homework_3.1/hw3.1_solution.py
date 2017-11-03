import pymongo

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")

# get a handle to the school database
db = connection.school
students = db.students


# function to count the number of students in the collection 
def student_count():
    query = {}
    try:
        total_count = students.find(query).count()
    except Exception as ex:
        print "Unexpected Error: ", type(ex), ex
    return total_count


# function to find the  student details
def remove_lowest_homework(stu_count):
    for i in range(0, stu_count):
        max_score = 0
        scores_list = []
        query = {'_id': i, 'scores.type': 'homework'}
        projection = {'scores': 1, '_id': 0}
        try:
            # Finding the homework scores
            cursor = students.find_one(query, projection)
        except Exception as ex:
            print "Unexpected Error: ", type(ex), ex
        # Comparing and retaining the max scores
        for doc in cursor['scores']:
            if doc['type'] == 'homework':
                if max_score < doc['score']:
                    max_score = doc['score']
            else:
                scores_list.append(doc)  # adding scores of other than homework type
        scores_list.append({"score": max_score, "type": "homework"})
        # updating scores_list values in database
        students.update_one({'_id': i}, {'$set': {'scores': scores_list}})


if __name__ == '__main__':
    count = student_count()
    print(count)
    remove_lowest_homework(count)