# MVP 기능 명세

## 1차 목표

localhost에서 다음 기능이 동작해야 한다.

1. 메인 페이지 접속
2. 분석 대상 종목 목록 표시
3. 각 종목의 최신 뉴스공탐지수 표시
4. 종목 상세 페이지 접속
5. 날짜별 뉴스공탐지수 표 표시
6. Chart.js로 날짜별 지수 차트 표시
7. 관련 기사 목록 표시

## URL 설계

| URL | 역할 |
|---|---|
| `/` | 메인 페이지 |
| `/assets` | 종목 목록 페이지 |
| `/assets/{id}` | 종목 상세 페이지 |
| `/api/assets/{id}/index` | 날짜별 뉴스공탐지수 JSON |
| `/api/assets/{id}/articles` | 기사 목록 JSON |

## 화면 1: 메인/종목 목록

표시할 정보:

- 종목명
- 시장 구분
- 최신 분석일
- 최신 뉴스공탐지수
- 라벨
- 상세 페이지 링크

## 화면 2: 종목 상세

표시할 정보:

- 종목명, 코드, 시장 구분
- 날짜별 뉴스공탐지수 차트
- 날짜별 지수 표
- 관련 기사 목록

## API 응답 예시

`GET /api/assets/1/index`

```json
[
  {
    "targetDate": "2023-12-01",
    "fearGreedScore": 62.3,
    "indexLabel": "GREED",
    "articleCount": 100
  }
]
```

`GET /api/assets/1/articles`

```json
[
  {
    "title": "삼성전자 관련 기사 제목",
    "press": "경제신문",
    "publishedAt": "2023-12-01T09:30:00",
    "sentimentScore": 0.71,
    "sentimentLabel": "POSITIVE"
  }
]
```

## 1차 MVP 제외 범위

- 로그인
- 관리자 화면
- 실시간 크롤링 버튼
- 자동 배치
- AWS 배포
- Docker
- React
- Spring Security
