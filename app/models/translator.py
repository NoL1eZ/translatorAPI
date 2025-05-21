from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.backend.db import Base


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    discord = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    roles = relationship(
        "Role",
        secondary="assignments",
        back_populates="person",
        lazy="dynamic"
    )
    is_active = Column(Boolean, default=True)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    archive = Column(Boolean, default=False)
    person = relationship(
        "Person",
        secondary="assignments",
        back_populates="roles",
        lazy="dynamic"
    )