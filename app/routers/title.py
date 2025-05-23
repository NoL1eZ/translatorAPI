from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from slugify import slugify

from sqlalchemy.orm import selectinload

from app.schemas import CreateTitle, TeamResponse, MemberResponse, TeamMember
from app.models.title import Title
from app.models.assignments import Assignment
from app.backend.db_depends import get_db

router = APIRouter(prefix="/titles", tags=["titles"])

async def search_title(db: Annotated[AsyncSession, Depends(get_db)], slug: str):
    return await db.scalar(select(Title).where(Title.slug == slug))


@router.post("/")
async def create_title(db: Annotated[AsyncSession, Depends(get_db)], create_title: CreateTitle):
    title_slug = slugify(create_title.name)
    if search_title(db, title_slug):
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='Title with this name already exists'
        )

    title = Title(name=create_title.name,
                  description=create_title.description,
                  ongoing=create_title.ongoing,
                  slug=title_slug)

    db.add(title)
    await db.commit()
    await db.refresh(title)
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get("/")
async def get_titles(db: Annotated[AsyncSession, Depends(get_db)], ongoing: bool = True):
    query = select(Title)
    if ongoing:
        query = query.where(Title.ongoing == True)
    result = await db.scalars(query)
    return result.all()

@router.get("/{title_slug}")
async def get_title(db: Annotated[AsyncSession, Depends(get_db)], title_slug: str):
    if search_title(db, title_slug) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Title not exists'
        )



@router.patch("/{title_slug}")
async def update_title(db: Annotated[AsyncSession, Depends(get_db)], title_slug: str, update_title_model: CreateTitle ):
    title_update = await search_title(db, title_slug)
    if title_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Title not found'
        )
    title_update. name = update_title_model.name
    title_update. description = update_title_model.description
    title_update. ongoing = update_title_model.ongoing
    title_update. slug = slugify(update_title_model.name)

    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Successful'
    }

@router.delete("/{title_slug}")
async def delete_title(
        db: Annotated[AsyncSession, Depends(get_db)],
        title_slug: str
):
    title_to_delete = await search_title(db, title_slug)
    if title_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Title not found'
        )

    await db.delete(title_to_delete)
    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Delete successful'
    }


@router.get("/{title_slug}/team", response_model=TeamResponse)
async def get_title_team(
        title_slug: str,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Получить текущую команду тайтла по его slug

    Возвращает:
    - Информацию о тайтле
    - Список активных назначений с деталями людей и их ролей
    """
    # Находим тайтл по slug
    title_result = await db.execute(
        select(Title)
        .where(Title.slug == title_slug)
    )
    title = title_result.scalar_one_or_none()

    if not title:
        raise HTTPException(
            status_code=404,
            detail="Title not found"
        )

    # Получаем активные назначения с деталями
    assignments = await db.execute(
        select(Assignment)
        .options(
            selectinload(Assignment.person),
            selectinload(Assignment.role)
        )
        .where(
            Assignment.title_id == title.id,
        )
        .order_by(Assignment.role_id)
    )

    return TeamResponse(
        title_id=title.id,
        title_name=title.name,
        title_slug=title.slug,
        members=[
            {
                "person_id": a.person.id,
                "person_name": a.person.name,
                "person_discord": a.person.discord,
                "role_id": a.role.id,
                "role_name": a.role.name,
                "is_main": a.is_main
            }
            for a in assignments.scalars()
        ]
    )


