from strands import tool

from utils.catalog import get_course_details


@tool
def tool_get_course_details(course_id):
    """Return complete details for one course."""
    return get_course_details(course_id)
