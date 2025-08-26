from fastapi import APIRouter
from app.schemas.response import ApiSuccess


router = APIRouter()


@router.get("/", summary="Ping API")
async def ping() -> ApiSuccess[dict[str, str]]:
    return ApiSuccess(message="pong", data={"message": "pong"})


