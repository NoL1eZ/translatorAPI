from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.schemas import CreateRole
from app.models.translator import Role

router = APIRouter(prefix="/roles", tags=["roles"])

async def search_title(db: Annotated[AsyncSession, Depends(get_db)], name: str):
    role = await db.scalar(select(Role).where(Role.name == name))
    if role:
        return role
    else:
        return None


@router.post("/")
async def create_role(db: Annotated[AsyncSession, Depends(get_db)], role_data: CreateRole):

    role = search_role(db, role_data.name)
    if role:
        raise HTTPException(status_code=200, detail="Role already exists")

    db_role = Role(name=role_data.name,archive= False)
    db.add(db_role)
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get("/")
async def get_roles(db: Annotated[AsyncSession, Depends(get_db)]):
    query = select(Role)

    result = await db.execute(query)
    return result.scalars().all()

@router.patch("/{role_id}")
async def update_role(db: Annotated[AsyncSession, Depends(get_db)], role_id: int, role_data: CreateRole):
    role = await db.scalar(select(Role).where(Role.id == role_id))
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    if role_data.archive:
        role.archive = True

    if role_data.name != role.name:
        role.name = role_data.name

    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is successful'
    }
