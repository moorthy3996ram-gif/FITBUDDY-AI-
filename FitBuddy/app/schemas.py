from typing import Literal
from pydantic import BaseModel, Field, field_validator

Intensity = Literal["low", "medium", "high"]

class UserInput(BaseModel):
    username: str = Field(min_length=2, max_length=120)
    user_id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, lt=500)
    goal: str = Field(min_length=2, max_length=80)
    intensity: Intensity
    @field_validator("username", "goal")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty")
        return value

class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=64)
    feedback: str = Field(min_length=3, max_length=2000)
