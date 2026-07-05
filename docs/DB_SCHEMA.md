# MVP DB Schema

## 설계 원칙

1. 분석 대상 자산은 `assets`에 한 번만 저장한다.
2. 기사 원본과 기사별 감성 결과는 `news_articles`에 저장한다.
3. 사용자가 빠르게 조회할 날짜별 평균 지수는 `daily_news_index`에 따로 저장한다.
4. Spring Boot는 분석하지 않고 조회만 한다.
5. Python은 분석하고 DB에 적재한다.

---

## 1. assets

분석 대상 종목/자산을 저장한다.

| 컬럼 | 의미 |
|---|---|
| id | 내부 PK |
| code | 종목 코드 또는 자산 코드 |
| name | 종목명/자산명 |
| market_type | KOSPI, KOSDAQ, CRYPTO, INDEX 등 |
| category | LARGE_CAP, SMALL_CAP, CRYPTO 등 |
| search_keyword | 뉴스 검색 키워드 |
| active | 분석 대상 사용 여부 |
| created_at | 생성 시각 |

예:

| code | name | market_type | category | search_keyword |
|---|---|---|---|---|
| 005930 | 삼성전자 | KOSPI | LARGE_CAP | 삼성전자 |
| BTC | 비트코인 | CRYPTO | CRYPTO | 비트코인 |
| KOSPI | 코스피 | INDEX | INDEX | 코스피 |

---

## 2. news_articles

크롤링한 기사와 기사별 감성 분석 결과를 저장한다.

| 컬럼 | 의미 |
|---|---|
| id | 내부 PK |
| asset_id | 분석 대상 자산 FK |
| title | 기사 제목 |
| press | 언론사 |
| url | 기사 URL |
| published_at | 기사 발행 시각 |
| crawled_at | 크롤링 시각 |
| summary | 기사 요약/본문 일부 |
| matched_sentence | 종목 키워드가 포함된 핵심 문장 |
| positive_count | 긍정 단어 수 |
| negative_count | 부정 단어 수 |
| sentiment_score | 0~1 감성 점수 |
| sentiment_label | POSITIVE, NEGATIVE, NEUTRAL |

---

## 3. daily_news_index

날짜별 종목별 뉴스 공포·탐욕 지수를 저장한다.

| 컬럼 | 의미 |
|---|---|
| id | 내부 PK |
| asset_id | 분석 대상 자산 FK |
| target_date | 분석 날짜 |
| article_count | 분석 기사 수 |
| positive_article_count | 긍정 기사 수 |
| negative_article_count | 부정 기사 수 |
| neutral_article_count | 중립 기사 수 |
| avg_sentiment_score | 기사별 감성 점수 평균 |
| fear_greed_score | 0~100 뉴스공탐지수 |
| index_label | EXTREME_FEAR, FEAR, NEUTRAL, GREED, EXTREME_GREED |
| buy_signal | 매수 참고 신호 |
| sell_signal | 매도 참고 신호 |

---

## 관계

```text
assets 1 : N news_articles
assets 1 : N daily_news_index
```

즉, 삼성전자라는 자산 하나에 여러 기사와 여러 날짜별 지수가 연결된다.

---

## 지수 라벨 기준 초안

`fear_greed_score`는 0~100 기준이다.

| 점수 구간 | 라벨 |
|---|---|
| 0 이상 25 미만 | EXTREME_FEAR |
| 25 이상 45 미만 | FEAR |
| 45 이상 55 이하 | NEUTRAL |
| 55 초과 75 이하 | GREED |
| 75 초과 100 이하 | EXTREME_GREED |

이 기준은 나중에 실제 데이터 분포를 보고 조정할 수 있다.

---

## 개발 순서

1. 이 3개 테이블만 먼저 구현한다.
2. 샘플 데이터로 화면을 띄운다.
3. Python 결과를 이 테이블에 넣는 스크립트를 만든다.
4. 이후 주가/RSI/MACD 비교가 필요하면 `daily_prices`, `technical_indicators`를 추가한다.
