from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.backend.db import Base

class Title(Base):
    __tablename__ = 'titles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text)
    ongoing = Column(Boolean, default=True)
    assignments = relationship("Assignment", back_populates="title")
    chapters = relationship("Chapter", back_populates="title")


class Chapter(Base):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True, index=True)
    title_id = Column(Integer, ForeignKey('titles.id'), nullable=False)

    # Основные атрибуты главы
    number = Column(Float, nullable=False)
    name = Column(String(200))
    content = Column(Text)
    status = Column(String(20), default="draft")

    # Даты
    created_at = Column(DateTime, default=datetime.now())
    published_at = Column(DateTime)

    # Внешние связи (relationship)
    title = relationship("Title", back_populates="chapters")
    substitutions = relationship("Substitution", back_populates="chapter")

