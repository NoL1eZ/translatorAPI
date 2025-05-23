from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


from app.models.assignments import Assignment
from app.models.title import Chapter
from app.models.substitution import Substitution
from app.schemas import CreateChapter
from app.backend.db_depends import get_db

router = APIRouter(prefix="/titles/{title_id}/chapters", tags=["chapters"])

@router.post("/")
async def create_chapter(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/")
async def get_chapters(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/{chapter_id}")
async def get_chapter(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.patch("/{chapter_id}")
async def update_chapter(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.delete("/{chapter_id}")
async def delete_chapter(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.post("/{chapter_id}/publish")
async def publish_chapter(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/{chapter_id}/history")
async def get_chapter_history(db: Annotated[AsyncSession, Depends(get_db)]):
    pass