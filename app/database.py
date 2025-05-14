from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from datetime import datetime


SQLALCHEMY_DATABASE_URL = "sqlite:///./manga.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    discord = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    roles = relationship(
        "Role",
        secondary="assignments",
        back_populates="people",
        lazy="dynamic"  
    )
    is_active = Column(Boolean, default=True)
    
class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    archive = Column(Boolean, default=False) 
    people = relationship(
        "Person",
        secondary="assignments",
        back_populates="roles",
        lazy="dynamic"
    )
    
class Title(Base):
    __tablename__ = 'titles'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text)
    ongoing = Column(Boolean, default=True)
    assignments = relationship("Assignment", back_populates="title")
    chapters = relationship("Chapter", back_populates="title")
    

class Assignment(Base):
    __tablename__ = 'assignments'
    
    id = Column(Integer, primary_key=True)
    title_id = Column(Integer, ForeignKey('titles.id'))
    person_id = Column(Integer, ForeignKey('people.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))
    is_main = Column(Boolean, default=True)  # Основной или замещающий
    
    # Связи
    title = relationship("Title", back_populates="assignments")
    person = relationship("Person")
    role = relationship("Role")
    substitutions = relationship("Substitution", back_populates="assignment")

class Substitution(Base):
    __tablename__ = 'substitutions'
    
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id'))
    substitute_id = Column(Integer, ForeignKey('people.id'))
    chapter_id = Column(Integer, ForeignKey('chapters.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    reason = Column(String(200))
    
    # Связи
    assignment = relationship("Assignment", back_populates="substitutions")
    substitute = relationship("Person")
    chapter = relationship("Chapter")
    
class Chapter(Base):
    __tablename__ = 'chapters'
    
    id = Column(Integer, primary_key=True, index=True)
    title_id = Column(Integer, ForeignKey('titles.id'), nullable=False)
    
    # Основные атрибуты главы
    number = Column(String(50), nullable=False)  # "Глава 1", "Vol. 3 Ch. 5"
    name = Column(String(200))                  # "Начало приключений"
    content = Column(Text)                      # Текст главы (если храним)
    status = Column(String(20), default="draft")# draft/published/archived
    
    # Даты
    created_at = Column(DateTime, server_default=func.now())
    published_at = Column(DateTime)
    
    # Внешние связи (relationship)
    title = relationship("Title", back_populates="chapters")
    substitutions = relationship("Substitution", back_populates="chapter")
