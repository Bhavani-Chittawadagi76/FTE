import json

def load_catalog():

    with open("data/catalog.json") as f:
        return json.load(f)

def search_catalog(keyword):

    catalog = load_catalog()

    results = []

    for item in catalog:

        if keyword.lower() in item["title"].lower():

            results.append(item)

    return results

def get_course_details(course_id):

    catalog = load_catalog()

    for course in catalog:

        if course["learningId"] == course_id:
            return course

    return None