from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import (
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    list_users,
    update_user,
)


router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(data: UserCreate, db: AsyncSession = Depends(get_db)) -> UserRead:
    if await get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, data)
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead)
async def get_user_endpoint(user_id: UUID, db: AsyncSession = Depends(get_db)) -> UserRead:
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.get("/", response_model=list[UserRead])
async def list_users_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> Sequence[UserRead]:
    users = await list_users(db, skip=skip, limit=limit)
    return [UserRead.model_validate(u) for u in users]


@router.put("/{user_id}", response_model=UserRead)
async def update_user_endpoint(
    user_id: UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    user = await update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(user_id: UUID, db: AsyncSession = Depends(get_db)) -> None:
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None


