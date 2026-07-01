from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models, schemas


def list_applications(
    db: Session,
    q: str | None = None,
    status: str | None = None,
    sort: str = "deadline",
) -> list[models.CompanyApplication]:
    statement = select(models.CompanyApplication)
    if q:
        keyword = f"%{q}%"
        statement = statement.where(
            models.CompanyApplication.company_name.like(keyword)
            | models.CompanyApplication.position.like(keyword)
            | models.CompanyApplication.memo.like(keyword)
        )
    if status:
        statement = statement.where(models.CompanyApplication.status == status)
    if sort == "created":
        statement = statement.order_by(models.CompanyApplication.created_at.desc())
    elif sort == "company":
        statement = statement.order_by(models.CompanyApplication.company_name)
    else:
        statement = statement.order_by(
            models.CompanyApplication.deadline.is_(None),
            models.CompanyApplication.deadline,
            models.CompanyApplication.created_at.desc(),
        )
    return list(db.scalars(statement))


def get_application(db: Session, application_id: int) -> models.CompanyApplication | None:
    return db.get(models.CompanyApplication, application_id)


def create_application(
    db: Session,
    application: schemas.ApplicationCreate,
) -> models.CompanyApplication:
    db_application = models.CompanyApplication(**application.model_dump())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def update_application(
    db: Session,
    db_application: models.CompanyApplication,
    application: schemas.ApplicationUpdate,
) -> models.CompanyApplication:
    update_data = application.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_application, field, value)
    db.commit()
    db.refresh(db_application)
    return db_application


def update_status(
    db: Session,
    db_application: models.CompanyApplication,
    status: schemas.ApplicationStatus,
) -> models.CompanyApplication:
    db_application.status = status
    db.commit()
    db.refresh(db_application)
    return db_application


def update_memo(
    db: Session,
    db_application: models.CompanyApplication,
    memo: str,
) -> models.CompanyApplication:
    db_application.memo = memo
    db.commit()
    db.refresh(db_application)
    return db_application


def delete_application(db: Session, db_application: models.CompanyApplication) -> None:
    db.delete(db_application)
    db.commit()


def get_dashboard_summary(db: Session) -> schemas.DashboardSummary:
    today = date.today()
    next_week = today + timedelta(days=7)
    applications = list_applications(db)
    status_counts = {
        status: 0
        for status in [
            "지원 예정",
            "지원 완료",
            "면접 예정",
            "면접 완료",
            "탈락",
            "합격",
        ]
    }
    for application in applications:
        status_counts[application.status] = status_counts.get(application.status, 0) + 1

    upcoming_deadlines = sum(
        1
        for application in applications
        if application.deadline and today <= application.deadline <= next_week
    )
    overdue = sum(
        1
        for application in applications
        if application.deadline
        and application.deadline < today
        and application.status not in ["지원 완료", "면접 예정", "면접 완료", "탈락", "합격"]
    )
    interviews = db.scalar(select(func.count()).select_from(models.InterviewRecord)) or 0

    return schemas.DashboardSummary(
        total=len(applications),
        upcoming_deadlines=upcoming_deadlines,
        overdue=overdue,
        interviews=interviews,
        status_counts=status_counts,
    )


def list_interviews(db: Session, application_id: int) -> list[models.InterviewRecord]:
    statement = (
        select(models.InterviewRecord)
        .where(models.InterviewRecord.application_id == application_id)
        .order_by(
            models.InterviewRecord.interview_date.is_(None),
            models.InterviewRecord.interview_date,
            models.InterviewRecord.created_at.desc(),
        )
    )
    return list(db.scalars(statement))


def get_interview(db: Session, interview_id: int) -> models.InterviewRecord | None:
    return db.get(models.InterviewRecord, interview_id)


def create_interview(
    db: Session,
    application_id: int,
    interview: schemas.InterviewCreate,
) -> models.InterviewRecord:
    db_interview = models.InterviewRecord(
        application_id=application_id,
        **interview.model_dump(),
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview


def update_interview(
    db: Session,
    db_interview: models.InterviewRecord,
    interview: schemas.InterviewUpdate,
) -> models.InterviewRecord:
    for field, value in interview.model_dump(exclude_unset=True).items():
        setattr(db_interview, field, value)
    db.commit()
    db.refresh(db_interview)
    return db_interview


def delete_interview(db: Session, db_interview: models.InterviewRecord) -> None:
    db.delete(db_interview)
    db.commit()


def list_cover_letters(
    db: Session,
    application_id: int,
) -> list[models.CoverLetterQuestion]:
    statement = (
        select(models.CoverLetterQuestion)
        .where(models.CoverLetterQuestion.application_id == application_id)
        .order_by(models.CoverLetterQuestion.created_at.desc())
    )
    return list(db.scalars(statement))


def get_cover_letter(
    db: Session,
    cover_letter_id: int,
) -> models.CoverLetterQuestion | None:
    return db.get(models.CoverLetterQuestion, cover_letter_id)


def create_cover_letter(
    db: Session,
    application_id: int,
    cover_letter: schemas.CoverLetterCreate,
) -> models.CoverLetterQuestion:
    db_cover_letter = models.CoverLetterQuestion(
        application_id=application_id,
        **cover_letter.model_dump(),
    )
    db.add(db_cover_letter)
    db.commit()
    db.refresh(db_cover_letter)
    return db_cover_letter


def update_cover_letter(
    db: Session,
    db_cover_letter: models.CoverLetterQuestion,
    cover_letter: schemas.CoverLetterUpdate,
) -> models.CoverLetterQuestion:
    for field, value in cover_letter.model_dump(exclude_unset=True).items():
        setattr(db_cover_letter, field, value)
    db.commit()
    db.refresh(db_cover_letter)
    return db_cover_letter


def delete_cover_letter(
    db: Session,
    db_cover_letter: models.CoverLetterQuestion,
) -> None:
    db.delete(db_cover_letter)
    db.commit()


def list_events(db: Session, application_id: int) -> list[models.ApplicationEvent]:
    statement = (
        select(models.ApplicationEvent)
        .where(models.ApplicationEvent.application_id == application_id)
        .order_by(
            models.ApplicationEvent.event_date.is_(None),
            models.ApplicationEvent.event_date.desc(),
            models.ApplicationEvent.created_at.desc(),
        )
    )
    return list(db.scalars(statement))


def get_event(db: Session, event_id: int) -> models.ApplicationEvent | None:
    return db.get(models.ApplicationEvent, event_id)


def create_event(
    db: Session,
    application_id: int,
    event: schemas.EventCreate,
) -> models.ApplicationEvent:
    db_event = models.ApplicationEvent(application_id=application_id, **event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(
    db: Session,
    db_event: models.ApplicationEvent,
    event: schemas.EventUpdate,
) -> models.ApplicationEvent:
    for field, value in event.model_dump(exclude_unset=True).items():
        setattr(db_event, field, value)
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, db_event: models.ApplicationEvent) -> None:
    db.delete(db_event)
    db.commit()
