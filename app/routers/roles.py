from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated, List
from sqlalchemy import insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


from app.backend.db_depends import get_db
from app.schemas import CreatePerson
from app.models.translator import Person, Role
from app.models.assignments import Assignment
from app.models.title import Title
from app.models.substitution import Substitution
from app.models.translator import Role

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/")
async def create_role(
        db: Annotated[AsyncSession, Depends(get_db)],
        name: str,
):
    db_role = Role(name=name)
    db.add(db_role)

    await db.commit()
    await db.refresh(db_role)

    return db_role


@router.get("/")
async def get_roles(
        db: Annotated[AsyncSession, Depends(get_db)],
):
    query = select(Role)

    result = await db.execute(query)
    return result.scalars().all()

@router.patch("/{role_id}", response_model=RoleRead)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db)
):
    # Реализация обновления роли
    pass