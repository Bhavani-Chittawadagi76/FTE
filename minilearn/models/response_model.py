from pydantic import BaseModel
from typing import List

class LearningResponse(BaseModel):
    type: str
    title: str
    learning_ids: List[str]
    message: str
    next_step_questions: List[str]