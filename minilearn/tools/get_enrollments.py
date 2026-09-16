from strands import tool

from utils.store import load_enrollments


@tool
def tool_get_enrollments():
    """List the learner's enrolled course IDs."""
    return load_enrollments()
