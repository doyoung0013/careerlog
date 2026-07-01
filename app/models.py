from datetime import datetime

from sqlalchemy import Date, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

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
