from strands import tool

from utils.catalog import load_catalog


@tool
def tool_popular_courses():
    """Return the leading recommendations from the local catalog."""
    return load_catalog()[:2]
