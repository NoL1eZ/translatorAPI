from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Annotated

from app.models.assignments import Assignment
from app.schemas import CreateAssignment
from app.backend.db_depends import get_db


router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post("/")
async def create_assignment(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/titles/{title_id}")
async def get_title_assignments(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.delete("/{assignment_id}")
async def delete_assignment(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.get("/active")
async def get_active_assignments(db: Annotated[AsyncSession, Depends(get_db)]):
    pass

@router.patch("/{assignment_id}/status")
async def update_assignment_status(db: Annotated[AsyncSession, Depends(get_db)]):
    pass
