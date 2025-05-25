from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from starlette import status


from app.models.title import Chapter, Title
from app.schemas import CreateChapter
from app.backend.db_depends import get_db

router = APIRouter(prefix="/titles/{title_slug}/chapters", tags=["chapters"])


async def search_chapter(db: Annotated[AsyncSession, Depends(get_db)], title_slug: str, chapter_id: int):
    return await db.scalar(select(Chapter).join(Title).where(Title.slug == title_slug, Chapter.id == chapter_id))

@router.post("/")
async def create_chapter(db: Annotated[AsyncSession, Depends(get_db)], data: CreateChapter, title_slug: str):

    chapter = Chapter(number = data.number,
                      name = data.name,
                      content = data.content,
                      status = data.status)

    db.add(chapter)
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get("/")
async def get_chapters(db: Annotated[AsyncSession, Depends(get_db)], title_slug: str, chapter_status: str = None):
    chapter = select(Chapter).join(Title).where(Title.slug == title_slug)
    if chapter_status is not None:
        chapter = chapter.where(Chapter.status == chapter_status)
    chapters = await db.scalar(chapter)
    result = chapters.all()
    if result:
        return result
    else:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chapters not found'
        )

@router.get("/{chapter_id}")
async def get_chapter(db: Annotated[AsyncSession, Depends(get_db)], title_slug: str, chapter_id: int):
    chapter = await search_chapter(db, title_slug, chapter_id)
    if chapter is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chapter not found'
        )
    return chapter

@router.patch("/{chapter_id}")
async def update_chapter(db: Annotated[AsyncSession, Depends(get_db)], title_slug: str, chapter_id: int, data: CreateChapter):
    search_chapter = await get_chapter(db, title_slug, chapter_id)

    if search_chapter is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chapter not found'
        )

    search_chapter.number = data.number
    search_chapter.name = data.name
    search_chapter.content = data.content
    search_chapter.status = data.status

    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is successful'
    }

@router.delete("/{chapter_id}")
async def delete_chapter(db: Annotated[AsyncSession, Depends(get_db)], title_slug: str, chapter_id: int):
        chapter_to_delete = await get_chapter(db, title_slug, chapter_id)
        if chapter_to_delete is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Chapter not found'
            )

        await db.delete(chapter_to_delete)
        await db.commit()

        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Delete successful'
        }

