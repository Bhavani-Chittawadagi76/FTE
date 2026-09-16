from strands import tool

from utils.catalog import search_catalog

@tool
def tool_search_courses(query):
    """Search the local course catalog by title, topic, level, or description."""
    return search_catalog(query)