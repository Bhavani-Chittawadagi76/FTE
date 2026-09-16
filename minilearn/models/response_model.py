from typing import List

from pydantic import BaseModel, Field

class LearningResponse(BaseModel):
    type: str = Field(
        default="answer",
        description="The response category, such as search or enrollment",
    )
    title: str = "MiniLearn response"
    learning_ids: List[str] = Field(default_factory=list)
    message: str = ""
    next_step_questions: List[str] = Field(default_factory=list)