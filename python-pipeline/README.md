# 독립 Python 일일 파이프라인

이 폴더는 Spring Boot와 분리되어 있습니다. Python이 네이버 뉴스 검색 결과를
수집해 CSV 두 개를 만들고, Spring Boot는 외부 API를 호출하지 않습니다.

## 왜 legacy HTML 크롤러를 사용하지 않는가

2026-07-11 실제 네이버 뉴스 검색 화면에서 legacy 선택자 `.news_tit`,
`.info.press`, `.api_txt_lines`가 모두 0건이었습니다. 현재 결과 클래스명도
난독화되어 있어 HTML 선택자에 다시 의존하면 쉽게 깨집니다.

따라서 공식 네이버 뉴스 검색 API를 사용합니다. 하루 호출 한도 안에서 종목별
최신 결과를 받고, 원하는 날짜만 Python에서 걸러 냅니다.

## 처음 한 번 준비

```bash
cd python-pipeline
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

`.env`에 네이버 개발자 센터에서 발급한 ID와 Secret을 입력합니다. 이 파일은
Git에 올리지 않습니다.

## 수동 실행

오전 9시 실행을 가정해 기본값은 전날 기사를 분석합니다.

```bash
python run_daily_pipeline.py
python run_daily_pipeline.py --date 2026-07-10
python run_daily_pipeline.py --date 2026-07-10 --asset-code 005930
```

결과:

- `output/news_articles.csv`
- `output/daily_news_index.csv`

같은 날짜를 다시 실행하면 날짜별 지수는 교체되고, 기사는 URL 기준으로
중복 제거됩니다.

## 오전 9시 자동 실행

MVP가 수동으로 끝까지 동작한 뒤 Windows 작업 스케줄러에 아래 작업을 매일
09:00으로 등록합니다.

```text
프로그램: D:\Projects\news-fear-greed-index\python-pipeline\.venv\Scripts\python.exe
인수: run_daily_pipeline.py
시작 위치: D:\Projects\news-fear-greed-index\python-pipeline
```

처음 3일 동안은 자동화보다 수동 실행과 결과 확인을 우선합니다.
