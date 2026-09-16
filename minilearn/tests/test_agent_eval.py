import json
import asyncio

import pytest

from config.settings import validate_config
from tools.enroll_course import tool_enroll
from tools.get_course_details import tool_get_course_details
from tools.get_enrollments import tool_get_enrollments
from tools.popular_courses import tool_popular_courses
from tools.search_courses import tool_search_courses
from tools.unenroll_course import tool_unenroll


def test_configuration_validator_accepts_required_values(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "test-model")

    assert validate_config() == {
        "GEMINI_API_KEY": "test-key",
        "GEMINI_MODEL": "test-model",
    }


def test_configuration_validator_reports_missing_values(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    with pytest.raises(ValueError, match="GEMINI_API_KEY, GEMINI_MODEL"):
        validate_config()


def test_search_courses_tool():
    assert tool_search_courses("python")[0]["learningId"] == "LRN002"


def test_course_details_tool():
    assert tool_get_course_details("LRN001")["title"] == "Machine Learning Basics"


def test_popular_courses_tool():
    assert len(tool_popular_courses()) == 2


def test_enrollment_tools(tmp_path, monkeypatch):
    enrollment_file = tmp_path / "enrollments.json"
    enrollment_file.write_text("[]")

    import utils.store as store

    monkeypatch.setattr(store, "FILE", str(enrollment_file))

    assert tool_enroll("LRN001") == ["LRN001"]
    assert tool_get_enrollments() == ["LRN001"]
    assert tool_unenroll("LRN001") == []
    assert json.loads(enrollment_file.read_text()) == []


def test_agent_stream_has_lifecycle_frames(monkeypatch):
    import agent
    from models.response_model import LearningResponse

    class FakeAgent:
        async def stream_async(self, prompt):
            yield {"data": "model event"}
            yield {"result": LearningResponse(message="done")}

    monkeypatch.setattr(agent, "build_agent", lambda: FakeAgent())

    async def collect_frames():
        return [frame async for frame in agent.stream_agent("find python")]

    frames = asyncio.run(collect_frames())
    assert frames[0]["type"] == "start"
    assert frames[-1]["type"] == "end"
    assert any(frame["type"] == "model_event" for frame in frames)
