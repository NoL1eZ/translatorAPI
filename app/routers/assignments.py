from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Annotated

from app.models.assignments import Assignment
from app.schemas import CreateAssignment
from app.backend.db_depends import get_db
from app.routers.title import search_title


router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post("/")
async def create_assignment(db: Annotated[AsyncSession, Depends(get_db)], data: CreateAssignment):
    assignments =  Assignment(title = data.title,
                                   person = data.person,
                                   role = data.role)
    db.add(assignments)
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.get("/titles/{title_slug}")
async def get_title_assignments(db: Annotated[AsyncSession, Depends(get_db)], title_slug: str):
    title = search_title(db, title_slug)
    if title is None:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='Title not exists'
        )

    assignments = await db.execute(select(Assignment).where(Assignment.title_id == title.id))
    result = assignments.all()
    return result


@router.delete("/{assignment_id}")
async def delete_assignment(db: Annotated[AsyncSession, Depends(get_db)], assignment_id: int):
    assignments = await db.execute(select(Assignment).where(Assignment.id == assignment_id))

    await db.delete(assignments)
    pass



