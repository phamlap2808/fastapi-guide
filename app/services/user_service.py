from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    new_user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=get_password_hash(data.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user(db: AsyncSession, user_id: UUID) -> User | None:
    return await db.get(User, str(user_id))


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def list_users(db: AsyncSession, skip: int = 0, limit: int = 50) -> Sequence[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def count_users(db: AsyncSession) -> int:
    result = await db.execute(select(func.count()).select_from(User))
    return int(result.scalar_one())


async def update_user(db: AsyncSession, user_id: UUID, data: UserUpdate) -> User | None:
    user = await get_user(db, user_id)
    if not user:
        return None

    if data.full_name is not None:
        user.full_name = data.full_name
    if data.is_active is not None:
        user.is_active = data.is_active
    if data.password is not None and data.password != "":
        user.hashed_password = get_password_hash(data.password)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
    user = await get_user(db, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True


