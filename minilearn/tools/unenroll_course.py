from strands import tool

from utils.store import unenroll


@tool
def tool_unenroll(course_id):
    """Remove the learner from a course by learning ID."""
    return unenroll(course_id)
