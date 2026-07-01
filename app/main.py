import csv
from datetime import datetime
from io import StringIO
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
APPLICATION_STATUSES = {"지원 예정", "지원 완료", "면접 예정", "면접 완료", "탈락", "합격"}

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


def get_child_or_404(child, application_id: int, message: str):
    if child is None or child.application_id != application_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return child


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


@app.get("/api/dashboard", response_model=schemas.DashboardSummary)
def get_dashboard(db: Session = Depends(get_db)):
    return crud.get_dashboard_summary(db)


@app.get("/api/applications", response_model=list[schemas.ApplicationRead])
def list_applications(
    q: str | None = None,
    status_filter: str | None = None,
    sort: str = "deadline",
    db: Session = Depends(get_db),
):
    return crud.list_applications(db, q=q, status=status_filter, sort=sort)


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


@app.get(
    "/api/applications/{application_id}/interviews",
    response_model=list[schemas.InterviewRead],
)
def list_interviews(application_id: int, db: Session = Depends(get_db)):
    get_application_or_404(application_id, db)
    return crud.list_interviews(db, application_id)


@app.post(
    "/api/applications/{application_id}/interviews",
    response_model=schemas.InterviewRead,
    status_code=status.HTTP_201_CREATED,
)
def create_interview(
    application_id: int,
    interview: schemas.InterviewCreate,
    db: Session = Depends(get_db),
):
    get_application_or_404(application_id, db)
    return crud.create_interview(db, application_id, interview)


@app.put(
    "/api/applications/{application_id}/interviews/{interview_id}",
    response_model=schemas.InterviewRead,
)
def update_interview(
    application_id: int,
    interview_id: int,
    interview: schemas.InterviewUpdate,
    db: Session = Depends(get_db),
):
    get_application_or_404(application_id, db)
    db_interview = get_child_or_404(
        crud.get_interview(db, interview_id),
        application_id,
        "면접 기록을 찾을 수 없습니다.",
    )
    return crud.update_interview(db, db_interview, interview)


@app.delete(
    "/api/applications/{application_id}/interviews/{interview_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_interview(
    application_id: int,
    interview_id: int,
    db: Session = Depends(get_db),
):
    get_application_or_404(application_id, db)
    db_interview = get_child_or_404(
        crud.get_interview(db, interview_id),
        application_id,
        "면접 기록을 찾을 수 없습니다.",
    )
    crud.delete_interview(db, db_interview)
    return None


@app.get(
    "/api/applications/{application_id}/cover-letters",
    response_model=list[schemas.CoverLetterRead],
)
def list_cover_letters(application_id: int, db: Session = Depends(get_db)):
    get_application_or_404(application_id, db)
    return crud.list_cover_letters(db, application_id)


@app.post(
    "/api/applications/{application_id}/cover-letters",
    response_model=schemas.CoverLetterRead,
    status_code=status.HTTP_201_CREATED,
)
def create_cover_letter(
    application_id: int,
    cover_letter: schemas.CoverLetterCreate,
    db: Session = Depends(get_db),
):
    get_application_or_404(application_id, db)
    return crud.create_cover_letter(db, application_id, cover_letter)


@app.put(
    "/api/applications/{application_id}/cover-letters/{cover_letter_id}",
    response_model=schemas.CoverLetterRead,
)
def update_cover_letter(
    application_id: int,
    cover_letter_id: int,
    cover_letter: schemas.CoverLetterUpdate,
    db: Session = Depends(get_db),
):
    get_application_or_404(application_id, db)
    db_cover_letter = get_child_or_404(
        crud.get_cover_letter(db, cover_letter_id),
        application_id,
        "자기소개서 문항을 찾을 수 없습니다.",
    )
    return crud.update_cover_letter(db, db_cover_letter, cover_letter)


@app.delete(
    "/api/applications/{application_id}/cover-letters/{cover_letter_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_cover_letter(
    application_id: int,
    cover_letter_id: int,
    db: Session = Depends(get_db),
):
    get_application_or_404(application_id, db)
    db_cover_letter = get_child_or_404(
        crud.get_cover_letter(db, cover_letter_id),
        application_id,
        "자기소개서 문항을 찾을 수 없습니다.",
    )
    crud.delete_cover_letter(db, db_cover_letter)
    return None


@app.get(
    "/api/applications/{application_id}/events",
    response_model=list[schemas.EventRead],
)
def list_events(application_id: int, db: Session = Depends(get_db)):
    get_application_or_404(application_id, db)
    return crud.list_events(db, application_id)


@app.post(
    "/api/applications/{application_id}/events",
    response_model=schemas.EventRead,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    application_id: int,
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
):
    get_application_or_404(application_id, db)
    return crud.create_event(db, application_id, event)


@app.put(
    "/api/applications/{application_id}/events/{event_id}",
    response_model=schemas.EventRead,
)
def update_event(
    application_id: int,
    event_id: int,
    event: schemas.EventUpdate,
    db: Session = Depends(get_db),
):
    get_application_or_404(application_id, db)
    db_event = get_child_or_404(
        crud.get_event(db, event_id),
        application_id,
        "타임라인 기록을 찾을 수 없습니다.",
    )
    return crud.update_event(db, db_event, event)


@app.delete(
    "/api/applications/{application_id}/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_event(
    application_id: int,
    event_id: int,
    db: Session = Depends(get_db),
):
    get_application_or_404(application_id, db)
    db_event = get_child_or_404(
        crud.get_event(db, event_id),
        application_id,
        "타임라인 기록을 찾을 수 없습니다.",
    )
    crud.delete_event(db, db_event)
    return None


@app.get("/api/applications.csv", include_in_schema=False)
def export_applications_csv(db: Session = Depends(get_db)):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["company_name", "position", "deadline", "status", "memo"])
    for application in crud.list_applications(db):
        writer.writerow(
            [
                application.company_name,
                application.position,
                application.deadline.isoformat() if application.deadline else "",
                application.status,
                application.memo,
            ]
        )
    filename = f"careerlog-{datetime.now().strftime('%Y%m%d')}.csv"
    return Response(
        content=output.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/applications/import-csv")
def import_applications_csv(
    payload: schemas.CsvImportRequest,
    db: Session = Depends(get_db),
):
    reader = csv.DictReader(StringIO(payload.csv_text))
    required = {"company_name", "position"}
    if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV에는 company_name, position 컬럼이 필요합니다.",
        )

    imported = 0
    for row in reader:
        company_name = (row.get("company_name") or "").strip()
        position = (row.get("position") or "").strip()
        if not company_name or not position:
            continue

        deadline = (row.get("deadline") or "").strip() or None
        row_status = (row.get("status") or "지원 예정").strip() or "지원 예정"
        if row_status not in APPLICATION_STATUSES:
            row_status = "지원 예정"
        application = schemas.ApplicationCreate(
            company_name=company_name,
            position=position,
            deadline=deadline,
            status=row_status,
            memo=row.get("memo") or "",
        )
        crud.create_application(db, application)
        imported += 1

    return {"imported": imported}
