from pydantic import BaseModel
from typing import List

from app.models.assignments import Assignment


class CreatePerson(BaseModel):
    name: str
    discord: str

class CreateTitle(BaseModel):
    name: str
    description: str | None = None
    ongoing: bool

class CreateAssignment(BaseModel):
    title: int
    translator: int
    role: int

class CreateChapter(BaseModel):
    number: float
    name: str
    content: str
    status: str

class CreateSubstitution(BaseModel):
    assignment_id: int
    substitute_id: int
    chapter_id: int
    reason: str | None