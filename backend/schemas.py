from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: str
    role: Optional[str] = None
    experience: Optional[str] = None


class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    priority: str = "Medium"
    task_type: Optional[str] = None
    estimated_hours: float = 1.0
    deadline: Optional[str] = None
    github_issue: Optional[str] = None
    project_id: int


class CheckInCreate(BaseModel):
    user_id: int
    date: str
    sleep_hours: Optional[float] = None
    stress_level: Optional[float] = None
    energy_level: Optional[float] = None


class FeedbackCreate(BaseModel):
    user_id: int
    task_id: Optional[int] = None
    rating: Optional[float] = None
    comment: Optional[str] = None
    actual_hours: Optional[float] = None