from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import init_engine, engine
from app.models.base import Base
from app.schemas.response import ApiError


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

    # Exception handlers chuẩn hóa
    @app.exception_handler(HTTPException)  # type: ignore[misc]
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        payload: ApiError[dict[str, object]] = ApiError(
            message=exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            code=exc.status_code,
            error={
                "path": str(request.url),
                "detail": exc.detail,
            },
        )
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

    @app.exception_handler(RequestValidationError)  # type: ignore[misc]
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        payload: ApiError[dict[str, object]] = ApiError(
            message="Validation Error",
            code=422,
            error={
                "path": str(request.url),
                "errors": exc.errors(),
            },
        )
        return JSONResponse(status_code=422, content=payload.model_dump())
    @app.exception_handler(Exception)  # type: ignore[misc]
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        # code mặc định cho lỗi không đoán trước
        payload: ApiError[dict[str, str]] = ApiError(
            message=str(exc) if settings.debug else "Internal Server Error",
            code=500,
            error={"path": str(request.url)}
        )
        return JSONResponse(status_code=500, content=payload.model_dump())

    return app


app = create_app()


