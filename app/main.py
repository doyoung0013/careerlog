from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CareerLog", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def get_application_or_404(application_id: int, db: Session):
    application = crud.get_application(db, application_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="지원 기업을 찾을 수 없습니다.",
        )
    return application


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post(
    "/api/applications",
    response_model=schemas.ApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
):
    return crud.create_application(db, application)


@app.get("/api/applications", response_model=list[schemas.ApplicationRead])
def list_applications(db: Session = Depends(get_db)):
    return crud.list_applications(db)


@app.get("/api/applications/{application_id}", response_model=schemas.ApplicationRead)
def get_application(application_id: int, db: Session = Depends(get_db)):
    return get_application_or_404(application_id, db)


@app.put("/api/applications/{application_id}", response_model=schemas.ApplicationRead)
def update_application(
    application_id: int,
    application: schemas.ApplicationUpdate,
    db: Session = Depends(get_db),
):
    db_application = get_application_or_404(application_id, db)
    return crud.update_application(db, db_application, application)


@app.patch(
    "/api/applications/{application_id}/status",
    response_model=schemas.ApplicationRead,
)
def update_application_status(
    application_id: int,
    status_update: schemas.StatusUpdate,
    db: Session = Depends(get_db),
):
    db_application = get_application_or_404(application_id, db)
    return crud.update_status(db, db_application, status_update.status)


@app.patch(
    "/api/applications/{application_id}/memo",
    response_model=schemas.ApplicationRead,
)
def update_application_memo(
    application_id: int,
    memo_update: schemas.MemoUpdate,
    db: Session = Depends(get_db),
):
    db_application = get_application_or_404(application_id, db)
    return crud.update_memo(db, db_application, memo_update.memo)


@app.delete("/api/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_application = get_application_or_404(application_id, db)
    crud.delete_application(db, db_application)
    return None
