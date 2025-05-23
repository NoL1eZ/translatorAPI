from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Annotated

from app.schemas import CreateTitle
from app.models.title import Title, Chapter
from app.models.assignments import Assignment
from app.backend.db_depends import get_db

router = APIRouter(prefix="/titles", tags=["titles"])

@router.post("/")
async def create_title(db: Annotated[AsyncSession, Depends(get_db)],
):
    pass

@router.get("/")
async def get_titles(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/{title_id}")
async def get_title(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.patch("/{title_id}")
async def update_title(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.delete("/{title_id}")
async def delete_title(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/{title_id}/team")
async def get_title_team(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/{title_id}/timeline")
async def get_title_timeline(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.post("/{title_id}/archive")
async def archive_title(db: Annotated[AsyncSession, Depends(get_db)]):
    pass