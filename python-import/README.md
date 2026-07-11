# Python Import Starter

이 폴더는 Python 분석 결과를 MySQL에 넣는 독립 적재기입니다.

처음 목표:

```text
Excel/CSV 분석 결과
→ pandas로 읽기
→ MySQL assets/news_articles/daily_news_index에 insert
```

Spring Boot가 Python이나 외부 API를 호출하지 않도록 역할을 분리합니다.

## 설치 예시

```bash
pip install -r requirements.txt
```

## 환경변수

`.env.example`을 복사해서 `.env`를 만들고 값을 채웁니다.

```text
DB_HOST=localhost
DB_PORT=3306
DB_NAME=news_fear_greed
DB_USER=root
DB_PASSWORD=your_password
```

## 실제 파이프라인 결과 적재

먼저 `db/schema_mvp.sql`로 데이터베이스와 테이블을 만든 다음 실행합니다.

```bash
cd python-import
python import_pipeline_csv_to_mysql.py
```

한 번 실행할 때 `assets`, `daily_news_index`, `news_articles`를 하나의
트랜잭션으로 적재합니다. 중간에 실패하면 해당 실행의 변경을 롤백합니다.
