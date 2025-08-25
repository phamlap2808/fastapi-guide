from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


engine = None
async_session_maker: async_sessionmaker[AsyncSession] | None = None


def init_engine() -> None:
    global engine, async_session_maker
    if settings.database_url:
        engine = create_async_engine(settings.database_url, future=True, echo=settings.debug)
        async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if async_session_maker is None:
        init_engine()
        if async_session_maker is None:  # pragma: no cover - bảo vệ khi thiếu DATABASE_URL
            raise RuntimeError("Database is not configured. Set APP_DATABASE_URL")

    assert async_session_maker is not None
    async with async_session_maker() as session:
        yield session


