from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship


from app.backend.db import Base

class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True)
    title_id = Column(Integer, ForeignKey('titles.id'))
    person_id = Column(Integer, ForeignKey('person.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))
    is_main = Column(Boolean, default=True)  # Основной или замещающий

    # Связи
    title = relationship("Title", back_populates="assignments")
    person = relationship("Person")
    role = relationship("Role")
    substitutions = relationship("Substitution", back_populates="assignment")