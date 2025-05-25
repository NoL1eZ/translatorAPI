from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy import insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession


from app.backend.db_depends import get_db
from app.schemas import CreatePerson
from app.models.translator import Person, Role
from app.models.assignments import Assignment
from app.models.substitution import Substitution


router = APIRouter(prefix='/translator', tags=['translator'])

async def search_person(db: Annotated[AsyncSession, Depends(get_db)], discord: str):
    person = await db.scalar(select(Person).where(Person.discord == discord))
    if person:
        return person
    else:
        return None



@router.post('/')
async def create_person(db: Annotated[AsyncSession, Depends(get_db)], person_data: CreatePerson) -> dict:

    if search_person(db, person_data.discord):
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='Person already exists'
        )
    # Создаем человека
    db_person = Person(name=person_data.name,
                       discord=person_data.discord,
                       is_active=True)
    db.add(db_person)
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/')
async def get_people(db: Annotated[AsyncSession, Depends(get_db)], all: bool = False):
    query = select(Person)
    if not all:
        query = query.where(Person.is_active == True)
    result = await db.scalars(query)
    return result.all()

@router.delete('/{discord}')
async def delete_person(db: Annotated[AsyncSession, Depends(get_db)], discord: str):
    person = search_person(db, discord)

    # Check if person exists and is active
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Person not found'
        )

    if not person.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Person is already inactive'
        )

    # Soft delete by marking as inactive
    person.is_active = False
    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'detail': 'Person deactivated successfully'

    }
@router.put('/{discord}/rezero')
async def rezero_person(db: Annotated[AsyncSession, Depends(get_db)], discord: str):
    person = search_person(db, discord)

    # Check if person exists and is active
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Person not found'
        )

    if person.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Person is already active'
        )

    # Soft delete by marking as inactive
    person.is_active = True
    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'detail': 'Person deactivated successfully'
    }


@router.get("/{discord}/assignments")
async def get_person_assignments(db: Annotated[AsyncSession, Depends(get_db)], discord: str):
    person = search_person(db, discord)
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Person not found'
        )

    assignments = await db.scalars(select(Assignment).where(Assignment.person_id == person.id))

    return assignments.all()

@router.get("/{discord}/substitutions")
async def get_person_substitutions(db: Annotated[AsyncSession, Depends(get_db)], discord: str):

    person = search_person(db, discord)
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Person not found'
        )

    result = await db.execute(select(Substitution).where(Substitution.person_id == person.id))
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='There is no substitution found'
        )
    return result.scalars().all()


@router.get("/{discord}/workload")
async def get_person_workload(db: Annotated[AsyncSession, Depends(get_db)], discord: str):
    # Находим человека по Discord
    person = await search_person(db, discord)
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )

    # Получаем все активные назначения с дополнительной информацией
    assignments = await db.scalars(select(Assignment).where(Assignment.person_id == person.id))

    # Получаем все подмены, где этот человек выступает заместителем
    substitutions = await db.execute(select(Substitution).join(Assignment)
                                     .where(Substitution.substitute_id == person.id))

    active_assignments = assignments.scalars().all(),
    active_substitutions = substitutions.scalars().all()

    return {"active_assignments": active_assignments,
            "active_substitutions": active_substitutions}



