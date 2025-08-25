from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import init_engine, engine
from app.models.base import Base


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan_context(app: FastAPI):
        # Khởi tạo engine và tạo bảng khi ở môi trường dev
        init_engine()
        if engine is not None and settings.env.lower() == "dev":
            async with engine.begin() as conn:  # type: ignore[union-attr]
                await conn.run_sync(Base.metadata.create_all)
        yield

    app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan_context)

    # CORS cho frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # chỉnh theo domain thực tế
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Healthcheck đơn giản
    @app.get("/health", tags=["health"])  # type: ignore[misc]
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    # API v1
    app.include_router(api_router, prefix=settings.api_v1_str)

    return app


app = create_app()


