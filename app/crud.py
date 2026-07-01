from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def list_applications(db: Session) -> list[models.CompanyApplication]:
    statement = select(models.CompanyApplication).order_by(
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
