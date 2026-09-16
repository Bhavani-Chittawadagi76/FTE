from strands import tool

from utils.store import enroll


@tool
def tool_enroll(course_id):
    """Enroll the learner in a course by learning ID."""
    return enroll(course_id)
