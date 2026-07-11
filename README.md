# 뉴스공탐지수 (News Fear & Greed Index)

한국어 금융 뉴스를 매일 수집하고, 종목별 뉴스 감성 점수를 0~100 공포·탐욕
지수로 집계해 Spring Boot 웹 화면에서 조회하는 로컬 MVP입니다.

## 현재 구현 범위

```text
네이버 뉴스 검색 API
  → 독립 Python 파이프라인
  → news_articles.csv / daily_news_index.csv
  → 독립 MySQL 적재기
  → MySQL 3개 테이블
  → Spring Boot + JPA 조회
  → Thymeleaf + Chart.js 화면
```

Spring Boot는 뉴스 수집이나 감성 분석을 하지 않습니다. Python 결과를 MySQL에
적재한 뒤 읽기만 하므로 각 단계의 오류를 분리해서 확인할 수 있습니다.

## legacy 크롤러 판정

기존 노트북의 네이버 HTML 선택자는 2026-07-11 현재 검색 결과와 맞지 않습니다.

- `.news_tit`: 0건
- `.info.press`: 0건
- `.api_txt_lines`: 0건

현재 검색 결과 클래스명은 난독화되어 있어 새 선택자에 다시 의존하지 않고,
공식 네이버 뉴스 검색 API를 Python 수집 단계에서만 사용합니다.

## 3일 로컬 MVP

### 1일차: 샘플 DB와 Spring 화면

1. MySQL을 실행합니다.
2. `db/schema_mvp.sql`을 실행합니다.
3. 먼저 화면만 볼 때는 `db/seed_sample.sql`도 실행합니다.
4. `spring-app`에서 Spring Boot를 실행합니다.
5. `http://localhost:8080`을 확인합니다.

### 2일차: 실제 뉴스 CSV와 DB 적재

1. 네이버 개발자 센터에서 검색 API ID/Secret을 발급합니다.
2. `python-pipeline/.env.example`을 `.env`로 복사해 값을 입력합니다.
3. `python run_daily_pipeline.py --date YYYY-MM-DD`를 실행합니다.
4. `python-import/.env.example`을 `.env`로 복사해 MySQL 정보를 입력합니다.
5. `python import_pipeline_csv_to_mysql.py`를 실행합니다.
6. Spring 화면을 새로고침해 실제 결과를 확인합니다.

### 3일차: 반복 실행과 오전 9시 예약

1. 같은 날짜를 재실행해 중복이 생기지 않는지 확인합니다.
2. API JSON과 상세 화면을 확인합니다.
3. `scripts/run_daily_local.bat`의 경로를 확인합니다.
4. Windows 작업 스케줄러에 매일 오전 9시 작업을 등록합니다.

상세 체크리스트는 `docs/THREE_DAY_LOCAL_MVP.md`에 있습니다.

## 처음 한 번 설치

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\activate
pip install -r requirements-local.txt
```

Spring Boot는 Java 17과 MySQL 8을 기준으로 합니다.

```bash
cd spring-app
# Windows
gradlew.bat bootRun
```

## 주요 URL

| URL | 역할 |
|---|---|
| `http://localhost:8080/` | 종목 목록과 최신 지수 |
| `http://localhost:8080/assets/{id}` | 종목별 차트와 기사 |
| `http://localhost:8080/api/assets` | 종목 최신 지수 JSON |
| `http://localhost:8080/api/assets/{id}/index` | 날짜별 지수 JSON |
| `http://localhost:8080/api/assets/{id}/articles` | 기사 JSON |

## 이번 MVP에서 제외

React, Docker, AWS, RDS, Nginx, 로그인, Spring Security, 실시간 크롤링
버튼, Spring↔Python 직접 호출은 넣지 않습니다.

## 보안

`.env`, 네이버 Client Secret, MySQL 비밀번호는 Git에 커밋하지 않습니다.
