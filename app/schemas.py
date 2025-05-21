from pydantic import BaseModel
from typing import List

class Person(BaseModel):
    name: str
    discord: str
    roles: List[int]

class Title(BaseModel):
    name: str
    description: str | None = None
    ongoing: bool

class Assignment(BaseModel):
    title: int
    translator: int
    role: int

class Chapter(BaseModel):
    number: float
    name: str
    content: str
    status: str