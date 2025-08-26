from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.response import ApiSuccess
from app.schemas.pagination import OffsetLimitRequest, PaginationResponse
from app.services.user_service import (
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    list_users,
    update_user,
)


router = APIRouter()


@router.post("/", response_model=ApiSuccess[UserRead], status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(data: UserCreate, db: AsyncSession = Depends(get_db)) -> ApiSuccess[UserRead]:
    if await get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, data)
    return ApiSuccess(message="User created", code=201, data=UserRead.model_validate(user))


@router.get("/{user_id}", response_model=ApiSuccess[UserRead])
async def get_user_endpoint(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ApiSuccess[UserRead]:
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiSuccess(message="OK", code=200, data=UserRead.model_validate(user))


@router.get("/", response_model=ApiSuccess[PaginationResponse])
async def list_users_endpoint(
    pagination: OffsetLimitRequest = Depends(),
    db: AsyncSession = Depends(get_db),
) -> ApiSuccess[PaginationResponse]:
    users = await list_users(db, skip=pagination.skip, limit=pagination.limit)
    from app.services.user_service import count_users
    total = await count_users(db)
    payload = PaginationResponse(
        items=[UserRead.model_validate(u) for u in users],
        total_count=total,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    return ApiSuccess(message="OK", code=200, data=payload)


@router.put("/{user_id}", response_model=ApiSuccess[UserRead])
async def update_user_endpoint(
    user_id: UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> ApiSuccess[UserRead]:
    user = await update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiSuccess(message="User updated", code=200, data=UserRead.model_validate(user))


@router.delete("/{user_id}", response_model=ApiSuccess[dict], status_code=status.HTTP_200_OK)
async def delete_user_endpoint(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ApiSuccess[dict]:
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiSuccess(message="User deleted", code=200, data={"deleted": True, "user_id": str(user_id)})


