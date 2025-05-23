from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Annotated

from app.models.substitution import Substitution
from app.schemas import CreateSubstitution
from app.backend.db_depends import get_db

router = APIRouter(prefix="/substitutions", tags=["substitutions"])


@router.post("/")
async def create_substitution(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/chapters/{chapter_id}")
async def get_chapter_substitutions(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/assignments/{assignment_id}")
async def get_assignment_substitutions(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.post("/{substitution_id}/approve")
async def approve_substitution(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/stats")
async def get_substitution_stats(db: Annotated[AsyncSession, Depends(get_db)]):
    pass
