from fastapi import APIRouter


router = APIRouter()


@router.get("/", summary="Ping API")
async def ping() -> dict[str, str]:
    return {"message": "pong"}


