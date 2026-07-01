# CareerLog

취업 준비 과정에서 지원 기업과 기업별 메모를 관리하는 FastAPI 기반 MVP입니다.

## 구현 기능

- 지원 기업 생성
- 지원 기업 목록 조회
- 지원 기업 상세 조회
- 지원 기업 수정
- 지원 기업 삭제
- 지원 상태 변경
- 기업별 메모 저장

## 기술 스택

- FastAPI
- SQLite
- SQLAlchemy
- HTML, CSS, JavaScript

## 프로젝트 구조

```text
careerlog/
├─ app/
│  ├─ __init__.py
│  ├─ crud.py
│  ├─ database.py
│  ├─ main.py
│  ├─ models.py
│  └─ schemas.py
├─ static/
│  ├─ app.js
│  ├─ index.html
│  └─ styles.css
├─ README.md
└─ requirements.txt
```

## 실행 방법

가상환경을 만들고 의존성을 설치합니다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell에서는 다음처럼 활성화합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

개발 서버를 실행합니다.

```bash
uvicorn app.main:app --reload
```

브라우저에서 다음 주소로 접속합니다.

```text
http://127.0.0.1:8000
```

API 문서는 다음 주소에서 확인할 수 있습니다.

```text
http://127.0.0.1:8000/docs
```

## 데이터베이스

서버를 처음 실행하면 프로젝트 루트에 `careerlog.db` SQLite 파일이 생성됩니다.

현재 MVP에서는 지원 기업 정보와 기업별 메모를 하나의 테이블에서 관리합니다. 이후 상담/면접 기록과 자기소개서 문항을 별도 테이블로 확장하기 좋도록 백엔드 파일을 모델, 스키마, CRUD, 앱 진입점으로 나누어 두었습니다.
