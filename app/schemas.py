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


class DashboardSummary(BaseModel):
    total: int
    upcoming_deadlines: int
    overdue: int
    interviews: int
    status_counts: dict[str, int]


class InterviewBase(BaseModel):
    interview_date: date | None = None
    interview_type: str = Field(default="면접", min_length=1, max_length=60)
    result: str = Field(default="예정", min_length=1, max_length=60)
    questions: str = ""
    notes: str = ""


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(BaseModel):
    interview_date: date | None = None
    interview_type: str | None = Field(default=None, min_length=1, max_length=60)
    result: str | None = Field(default=None, min_length=1, max_length=60)
    questions: str | None = None
    notes: str | None = None


class InterviewRead(InterviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    created_at: datetime
    updated_at: datetime


class CoverLetterBase(BaseModel):
    question: str = Field(..., min_length=1)
    answer: str = ""
    status: str = Field(default="초안", min_length=1, max_length=30)


class CoverLetterCreate(CoverLetterBase):
    pass


class CoverLetterUpdate(BaseModel):
    question: str | None = Field(default=None, min_length=1)
    answer: str | None = None
    status: str | None = Field(default=None, min_length=1, max_length=30)


class CoverLetterRead(CoverLetterBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    created_at: datetime
    updated_at: datetime


class EventBase(BaseModel):
    event_date: date | None = None
    event_type: str = Field(..., min_length=1, max_length=60)
    note: str = ""


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    event_date: date | None = None
    event_type: str | None = Field(default=None, min_length=1, max_length=60)
    note: str | None = None


class EventRead(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    created_at: datetime
    updated_at: datetime


class CsvImportRequest(BaseModel):
    csv_text: str = Field(..., min_length=1)
