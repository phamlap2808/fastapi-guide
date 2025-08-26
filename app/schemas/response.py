from typing import Generic, Optional, TypeVar

from pydantic import BaseModel


T = TypeVar("T")
E = TypeVar("E")


class ApiSuccess(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Success"
    code: int = 0
    data: Optional[T] = None


class ApiError(BaseModel, Generic[E]):
    success: bool = False
    message: str = "Error"
    code: int = 1
    error: Optional[E] = None


ApiResponse = ApiSuccess[T] | ApiError[E]


