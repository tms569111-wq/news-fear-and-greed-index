# Codex용 프로젝트 인수인계 요약

## 프로젝트명

News-Fear-and-Greed-index  
한국어명: 뉴스공탐지수

## 한 줄 설명

뉴스 기사 감성 분석 결과를 종목별·날짜별 뉴스 공포·탐욕 지수로 계산하고, Spring Boot 웹사이트에서 조회하는 서비스입니다.

## 기존 프로젝트 배경

기존 UGRP 프로젝트는 Python으로 네이버 뉴스 기사를 크롤링하고, KoNLPy/Okt 기반 토큰화와 긍부정 단어 분석, Dense 신경망 기반 감성 분석을 통해 날짜별 감성 점수를 계산했습니다.

기존 흐름은 대략 다음과 같습니다.

```text
분석 대상 키워드 설정
→ 날짜 범위 생성
→ 네이버 뉴스 크롤링
→ 기사 제목/언론사/본문 또는 요약 수집
→ KoNLPy/Okt 토큰화
→ 긍정/부정 단어 카운트
→ Dense 신경망 또는 감성 계산 로직으로 0~1 점수 산출
→ 하루 기사들의 평균 감성 점수 계산
→ 기존에는 Excel로 저장
```

이번 프로젝트에서는 Excel 저장 중심 구조를 MySQL 저장 구조로 바꾸고, Spring Boot 웹서비스에서 조회합니다.

## 역할 분리

```text
Python = 뉴스 수집/분석/DB 적재
MySQL = 분석 결과 저장
Spring Boot = DB 조회/API/화면 렌더링
Thymeleaf + Chart.js = 웹 화면/차트
```

## 1차 MVP 목표

1. MySQL 3개 테이블 사용
   - assets
   - news_articles
   - daily_news_index

2. Spring Boot 웹서비스 생성
   - Java 17
   - Spring Boot
   - Spring Web
   - Spring Data JPA
   - MySQL
   - Thymeleaf
   - Chart.js

3. 화면
   - 메인 페이지: 종목 목록 + 최신 뉴스공탐지수
   - 종목 상세 페이지: 날짜별 지수 표 + Chart.js 차트 + 관련 기사 목록

4. 데이터
   - 처음에는 `data.sql` 또는 `db/seed_sample.sql` 샘플 데이터로 화면 확인
   - 이후 Python 결과를 MySQL에 적재

## 현재 금지 범위

React, Docker, AWS, RDS, Nginx, HTTPS, Spring Security, 로그인, 회원가입은 1차 MVP에서 제외합니다.

## Codex 작업 원칙

- 한 번에 전체 프로젝트를 과하게 만들지 말 것.
- 먼저 3개 테이블 기반 MVP를 완성할 것.
- 복잡한 아키텍처보다 실행 가능한 localhost 결과를 우선할 것.
- 모든 새 코드에는 신입 개발자가 이해할 수 있는 최소한의 주석을 달 것.
- README에는 실행 방법, DB 생성 방법, 화면 URL, API URL을 반드시 작성할 것.
