import json

FILE = "data/enrollments.json"

def load_enrollments():

    with open(FILE) as f:
        return json.load(f)

def save_enrollments(data):

    with open(FILE, "w") as f:
        json.dump(data, f)

def enroll(course_id):

    data = load_enrollments()

    if course_id not in data:

        data.append(course_id)

        save_enrollments(data)

    return data

def unenroll(course_id):

    data = load_enrollments()

    if course_id in data:

        data.remove(course_id)

        save_enrollments(data)

    return data