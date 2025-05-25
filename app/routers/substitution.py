from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.models.substitution import Substitution
from app.models.title import Chapter, Title
from app.schemas import CreateSubstitution
from app.backend.db_depends import get_db
from app.routers.chapters import search_chapter
from app.routers.title import search_title

router = APIRouter(prefix="/substitutions", tags=["substitutions"])


@router.post("/")
async def create_substitution(db: Annotated[AsyncSession, Depends(get_db)], data: CreateSubstitution):
    substitution = Substitution(assignment_id=data.assignment_id,
                                substitute_id=data.substitute_id,
                                chapter_id = data.chapter_id,
                                reason = data.reason)
    db.add(substitution)
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get("/{title_slug}/{chapter_id}")
async def get_chapter_substitutions(db: Annotated[AsyncSession, Depends(get_db)], title_slug: str, chapter_id: int):
    chapter = await search_chapter(db, title_slug, chapter_id)
    if chapter is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chapter not found'
        )
    substitution = await db.execute(select(Substitution).where(Substitution.chapter_id == chapter_id))
    result = substitution.all()
    return result




@router.get("/assignments/{assignment_id}")
async def delete_substitutions(db: Annotated[AsyncSession, Depends(get_db)], substitution_id: int):
    substitution = await db.execute(select(Substitution).where(Substitution.id == substitution_id))
    await db.delete(substitution)
    pass





