# CareerLog

취업 준비 과정을 한곳에서 관리하는 FastAPI 기반 지원 관리 앱입니다.

지원 기업, 마감일, 진행 상태, 면접 기록, 자기소개서 문항, 타임라인을 함께 기록할 수 있어 여러 채용 공고를 동시에 관리할 때 흐름을 놓치지 않도록 돕습니다.

## 주요 기능

### 지원 기업 관리

- 지원 기업 등록, 조회, 수정, 삭제
- 회사명, 직무, 마감일, 지원 상태, 메모 관리
- 지원 상태 빠른 변경
- 기업별 상세 메모 저장

### 목록 탐색

- 회사명, 직무, 메모 검색
- 지원 상태별 필터
- 마감일 가까운 순, 최근 등록 순, 회사명 순 정렬
- 마감일 기준 D-Day 표시

### 취업 준비 대시보드

- 전체 지원 수 요약
- 7일 내 마감 기업 수 표시
- 마감이 지난 지원 항목 표시
- 상태별 지원 현황 집계
- 전체 면접 기록 수 확인

### 기록 관리

- 기업별 면접 기록 관리
- 면접일, 면접 유형, 결과, 질문, 복기 메모 저장
- 자기소개서 문항과 답변 관리
- 자소서 작성 상태 관리: 초안, 수정 중, 제출 완료
- 지원 완료, 서류 결과, 면접, 최종 결과 등 타임라인 기록

### CSV 백업

- 지원 목록 CSV 내보내기
- CSV 파일로 지원 목록 가져오기

## 화면 구성

```text
상단
├─ 앱 제목
├─ CSV 가져오기 / 내보내기
└─ 새 기업 등록

대시보드
├─ 전체 지원
├─ 7일 내 마감
├─ 마감 지남
├─ 면접 기록
└─ 상태별 집계

본문
├─ 왼쪽: 지원 목록, 검색, 필터, 정렬
└─ 오른쪽: 기본 정보, 면접, 자소서, 타임라인 탭
```

## 기술 스택

| 영역 | 기술 |
| --- | --- |
| Backend | FastAPI |
| Database | SQLite, SQLAlchemy |
| Schema | Pydantic |
| Frontend | HTML, CSS, JavaScript |
| Server | Uvicorn |

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
├─ .gitignore
├─ README.md
└─ requirements.txt
```

## 실행 방법

### 1. 가상환경 생성

```bash
python -m venv .venv
```

### 2. 가상환경 활성화

macOS 또는 Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 개발 서버 실행

```bash
uvicorn app.main:app --reload
```

### 5. 브라우저에서 접속

```text
http://127.0.0.1:8000
```

API 문서는 다음 주소에서 확인할 수 있습니다.

```text
http://127.0.0.1:8000/docs
```

## CSV 가져오기 형식

CSV 가져오기는 다음 컬럼을 사용합니다.

```csv
company_name,position,deadline,status,memo
Example Corp,Backend Intern,2026-07-15,지원 예정,채용 공고 확인 필요
```

| 컬럼 | 필수 여부 | 설명 |
| --- | --- | --- |
| `company_name` | 필수 | 회사명 |
| `position` | 필수 | 지원 직무 |
| `deadline` | 선택 | 마감일, `YYYY-MM-DD` 형식 |
| `status` | 선택 | 지원 예정, 지원 완료, 면접 예정, 면접 완료, 탈락, 합격 |
| `memo` | 선택 | 기업별 메모 |

`status`가 비어 있거나 지원하지 않는 값이면 `지원 예정`으로 저장됩니다.

## 데이터베이스

서버를 처음 실행하면 프로젝트 루트에 `careerlog.db` SQLite 파일이 생성됩니다.

현재 사용하는 주요 테이블은 다음과 같습니다.

| 테이블 | 설명 |
| --- | --- |
| `company_applications` | 지원 기업 기본 정보 |
| `interview_records` | 기업별 면접 기록 |
| `cover_letter_questions` | 기업별 자기소개서 문항과 답변 |
| `application_events` | 지원 진행 타임라인 |

`careerlog.db`는 로컬 실행 데이터이므로 Git에는 포함하지 않습니다.

## 개발 메모

- 정적 화면은 `static/index.html`, `static/styles.css`, `static/app.js`에서 관리합니다.
- API 라우트는 `app/main.py`에 정의되어 있습니다.
- 데이터 모델은 `app/models.py`, 요청/응답 스키마는 `app/schemas.py`에서 관리합니다.
- 데이터 접근 로직은 `app/crud.py`에 모아두었습니다.
