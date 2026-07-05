# Python Import Starter

이 폴더는 기존 Python 분석 결과를 MySQL에 넣기 위한 스크립트를 둘 위치입니다.

처음 목표:

```text
Excel/CSV 분석 결과
→ pandas로 읽기
→ MySQL assets/news_articles/daily_news_index에 insert
```

아직 실시간 크롤링 자동화는 하지 않습니다.

## 설치 예시

```bash
pip install pandas pymysql python-dotenv openpyxl
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
