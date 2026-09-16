import json
from pathlib import Path

CATALOG_FILE = Path(__file__).resolve().parents[1] / "data" / "catalog.json"


def load_catalog():
    with CATALOG_FILE.open() as file:
        return json.load(file)


def search_catalog(keyword):
    normalized_keyword = keyword.lower()
    results = []
    title_matches = []
    for item in load_catalog():
        searchable = " ".join(
            str(item.get(field, ""))
            for field in ("title", "level", "description", "topics")
        ).lower()
        if normalized_keyword in searchable:
            results.append(item)
            if normalized_keyword in item["title"].lower():
                title_matches.append(item)
    return title_matches + [item for item in results if item not in title_matches]


def get_course_details(course_id):
    return next(
        (course for course in load_catalog() if course["learningId"] == course_id),
        None,
    )
