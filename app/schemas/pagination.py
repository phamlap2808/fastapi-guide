from pydantic import BaseModel, Field


class OffsetLimitRequest(BaseModel):
    offset: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(20, ge=1, le=1000, description="Number of items to return")

    @property
    def skip(self) -> int:
        return self.offset


class PaginationResponse(BaseModel):
    items: list
    total_count: int = Field(..., ge=0)
    offset: int = Field(..., ge=0)
    limit: int = Field(..., ge=1)


