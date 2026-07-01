from datetime import datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class CompanyApplication(Base):
    __tablename__ = "company_applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_name: Mapped[str] = mapped_column(String(120), index=True)
    position: Mapped[str] = mapped_column(String(120))
    deadline = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="지원 예정", index=True)
    memo: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    interviews: Mapped[list["InterviewRecord"]] = relationship(
        back_populates="application",
        cascade="all, delete-orphan",
    )
    cover_letters: Mapped[list["CoverLetterQuestion"]] = relationship(
        back_populates="application",
        cascade="all, delete-orphan",
    )
    events: Mapped[list["ApplicationEvent"]] = relationship(
        back_populates="application",
        cascade="all, delete-orphan",
    )


class InterviewRecord(Base):
    __tablename__ = "interview_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("company_applications.id", ondelete="CASCADE"),
        index=True,
    )
    interview_date = mapped_column(Date, nullable=True)
    interview_type: Mapped[str] = mapped_column(String(60), default="면접")
    result: Mapped[str] = mapped_column(String(60), default="예정")
    questions: Mapped[str] = mapped_column(Text, default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    application: Mapped[CompanyApplication] = relationship(back_populates="interviews")


class CoverLetterQuestion(Base):
    __tablename__ = "cover_letter_questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("company_applications.id", ondelete="CASCADE"),
        index=True,
    )
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(30), default="초안")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    application: Mapped[CompanyApplication] = relationship(back_populates="cover_letters")


class ApplicationEvent(Base):
    __tablename__ = "application_events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("company_applications.id", ondelete="CASCADE"),
        index=True,
    )
    event_date = mapped_column(Date, nullable=True)
    event_type: Mapped[str] = mapped_column(String(60))
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    application: Mapped[CompanyApplication] = relationship(back_populates="events")
