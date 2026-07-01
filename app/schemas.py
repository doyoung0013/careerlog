from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ApplicationStatus = Literal[
    "지원 예정",
    "지원 완료",
    "면접 예정",
    "면접 완료",
    "탈락",
    "합격",
]


class ApplicationBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=120)
    position: str = Field(..., min_length=1, max_length=120)
    deadline: date | None = None
    status: ApplicationStatus = "지원 예정"
    memo: str = ""


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    company_name: str | None = Field(default=None, min_length=1, max_length=120)
    position: str | None = Field(default=None, min_length=1, max_length=120)
    deadline: date | None = None
    status: ApplicationStatus | None = None
    memo: str | None = None


class StatusUpdate(BaseModel):
    status: ApplicationStatus


class MemoUpdate(BaseModel):
    memo: str = ""


class ApplicationRead(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
