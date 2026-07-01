# CareerLog

취업 준비 과정에서 지원 기업, 면접 기록, 자기소개서 문항, 진행 타임라인을 관리하는 FastAPI 기반 앱입니다.

## 구현 기능

- 지원 기업 생성
- 지원 기업 목록 조회
- 지원 기업 상세 조회
- 지원 기업 수정
- 지원 기업 삭제
- 지원 상태 변경
- 기업별 메모 저장
- 지원 목록 검색, 상태 필터, 정렬
- 마감일 D-Day 표시
- 상태별 대시보드와 7일 내 마감 요약
- 기업별 면접 기록 관리
- 기업별 자기소개서 문항과 답변 관리
- 지원 진행 타임라인 관리
- 지원 목록 CSV 가져오기/내보내기

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

지원 기업 정보는 `company_applications` 테이블에서 관리하고, 면접 기록, 자기소개서 문항, 타임라인은 별도 테이블로 관리합니다.

CSV 가져오기는 다음 컬럼을 사용합니다.

```text
company_name,position,deadline,status,memo
```

`company_name`과 `position`은 필수이며, `deadline`은 `YYYY-MM-DD` 형식을 사용합니다.
