"""Strands-powered learning discovery agent."""

import asyncio
import logging
import re
from typing import Any, AsyncIterator

from strands import Agent
from strands.event_loop._retry import ModelRetryStrategy
from strands.models import OpenAIModel

from config.prompts import SYSTEM_PROMPT
from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from models.response_model import LearningResponse
from tools.enroll_course import tool_enroll
from tools.get_course_details import tool_get_course_details
from tools.get_enrollments import tool_get_enrollments
from tools.popular_courses import tool_popular_courses
from tools.search_courses import tool_search_courses
from tools.unenroll_course import tool_unenroll

logger = logging.getLogger(__name__)

TOOLS = [
    tool_search_courses,
    tool_get_course_details,
    tool_popular_courses,
    tool_enroll,
    tool_unenroll,
    tool_get_enrollments,
]
SYSTEM_PROMPT_TEXT = SYSTEM_PROMPT.strip()
GEMINI_OPENAI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


def model_factory() -> OpenAIModel:
    """Build the configured Gemini model through Strands' OpenAI adapter."""
    return OpenAIModel(
        client_args={
            "api_key": GEMINI_API_KEY,
            "base_url": GEMINI_OPENAI_BASE_URL,
            "timeout": 10.0,
        },
        model_id=GEMINI_MODEL,
        params={"temperature": 0.2},
    )


def build_tools() -> list[Any]:
    """Return the six tools in a stable order for every invocation."""
    return list(TOOLS)


def build_agent() -> Agent:
    """Build one configured Strands agent for a request."""
    return Agent(
        model=model_factory(),
        tools=build_tools(),
        system_prompt=SYSTEM_PROMPT_TEXT,
        structured_output_model=LearningResponse,
        retry_strategy=ModelRetryStrategy(max_attempts=1),
    )


def _structured_response(value: Any) -> LearningResponse | None:
    if isinstance(value, LearningResponse):
        return value
    if isinstance(value, dict):
        for key in ("structured_output", "result"):
            if key in value:
                parsed = _structured_response(value[key])
                if parsed:
                    return parsed
    if hasattr(value, "structured_output"):
        return _structured_response(value.structured_output)
    if isinstance(value, str):
        try:
            return LearningResponse.model_validate_json(value)
        except ValueError:
            return None
    return None


def local_fallback_response(user_input: str) -> LearningResponse:
    """Answer common LMS requests from the local JSON tools when the model is unavailable."""
    normalized = user_input.strip().lower()
    course_id_match = re.search(r"\bLRN\d{3}\b", user_input, re.IGNORECASE)
    course_id = course_id_match.group(0).upper() if course_id_match else None

    if "unenroll" in normalized or "remove me" in normalized:
        if not course_id:
            return LearningResponse(type="unenroll", message="Tell me the learning ID to unenroll from, such as LRN002.")
        enrollments = tool_unenroll(course_id)
        return LearningResponse(type="unenroll", learning_ids=enrollments, message=f"You are unenrolled from {course_id}.")

    if "enrollment" in normalized or "my courses" in normalized:
        enrollments = tool_get_enrollments()
        return LearningResponse(type="enrollments", learning_ids=enrollments, message=f"Your enrolled courses: {', '.join(enrollments) or 'none yet'}.")

    if "enroll" in normalized or "join" in normalized:
        if not course_id:
            return LearningResponse(type="enroll", message="Tell me the learning ID to enroll in, such as LRN002.")
        enrollments = tool_enroll(course_id)
        return LearningResponse(type="enroll", learning_ids=enrollments, message=f"You are enrolled in {course_id}.")

    if course_id:
        course = tool_get_course_details(course_id)
        if course:
            return LearningResponse(type="details", title=course["title"], learning_ids=[course_id], message=f"{course['title']} is a {course['level']} course requiring about {course['durationHours']} hours.")
        return LearningResponse(type="details", message=f"I could not find {course_id} in the local catalog.")

    if any(word in normalized for word in ("popular", "trending", "recommend")):
        courses = tool_popular_courses()
    else:
        query = re.sub(r"\b(what|is|are|about|find|show|me|course|courses|learn|tell)\b", " ", normalized)
        query = re.sub(r"[^a-z0-9 ]", " ", query)
        courses = tool_search_courses(query.strip() or normalized)

    learning_ids = [course["learningId"] for course in courses]
    if not courses:
        return LearningResponse(type="search", message="I could not find matching courses in the local catalog.")
    titles = ", ".join(course["title"] for course in courses[:5])
    return LearningResponse(type="search", learning_ids=learning_ids, message=f"I found these courses: {titles}.")


async def stream_agent(user_input: str, identity: str = "anonymous") -> AsyncIterator[dict[str, Any]]:
    """Yield lifecycle frames around the model's Strands events."""
    logger.info("[STEP 1] Invocation received")
    try:
        logger.info("[STEP 2] Identity resolved: %s", identity)
        logger.info("[STEP 3] Model selected: %s", GEMINI_MODEL)
        logger.info("[STEP 4] Tools built: %d", len(TOOLS))
        agent = build_agent()
        yield {"type": "start", "identity": identity}
        logger.info("[STEP 5] Streaming started")
        async for event in agent.stream_async(user_input):
            yield {"type": "model_event", "event": event}
        logger.info("[STEP 6] Streaming finished")
        yield {"type": "end"}
    finally:
        logger.info("[STEP 7] Cleanup complete")


async def collect_agent_response(user_input: str, identity: str = "anonymous") -> LearningResponse:
    try:
        response = None
        text_parts: list[str] = []
        async for frame in stream_agent(user_input, identity):
            event = frame.get("event")
            response = _structured_response(event) or response
            if isinstance(event, dict):
                text = event.get("data") or event.get("text")
                if isinstance(text, str):
                    text_parts.append(text)
        if response:
            return response
        text = "".join(text_parts).strip()
        if text:
            try:
                return LearningResponse.model_validate_json(text)
            except ValueError:
                return LearningResponse(message=text)
        raise RuntimeError("The agent returned no structured response")
    except Exception:
        logger.warning("Model unavailable; using local LMS tool fallback", exc_info=True)
        return local_fallback_response(user_input)


def run_agent(user_input: str) -> str:
    """Synchronous compatibility wrapper for scripts and legacy callers."""
    return asyncio.run(collect_agent_response(user_input)).message
