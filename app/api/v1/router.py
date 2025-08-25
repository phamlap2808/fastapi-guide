from fastapi import APIRouter

from app.api.v1.endpoints import ping, users


api_router = APIRouter()
api_router.include_router(ping.router, tags=["ping"], prefix="/ping")
api_router.include_router(users.router, tags=["users"], prefix="/users")


