from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


from app.backend.db import Base

class Substitution(Base):
    __tablename__ = 'substitutions'

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id'))
    substitute_id = Column(Integer, ForeignKey('person.id'))
    chapter_id = Column(Integer, ForeignKey('chapters.id'))
    reason = Column(String(200))

    # Связи
    assignment = relationship("Assignment", back_populates="substitutions")
    substitute = relationship("Person")
    chapter = relationship("Chapter")

