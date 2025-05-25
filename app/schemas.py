from pydantic import BaseModel
from typing import List

from app.models.assignments import Assignment


class CreatePerson(BaseModel):
    name: str
    discord: str

class CreateTitle(BaseModel):
    name: str
    description: str | None = None
    ongoing: bool = True

class CreateAssignment(BaseModel):
    title: int
    person: int
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

class CreateRole(BaseModel):
    name: str
    archive: bool = False

class MemberResponse(BaseModel):
    person_id: int
    person_name: str
    person_discord: str
    role_id: int
    role_name: str
    is_main: bool

class TeamResponse(BaseModel):
    title_id: int
    title_name: str
    title_slug: str
    members: List[MemberResponse]

class TeamMember(BaseModel):
    person_id: int
    person_name: str
    person_discord: str
    role_id: int
    role_name: str
    is_main: bool