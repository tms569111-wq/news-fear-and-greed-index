# News-Fear-and-Greed-index 프로젝트 컨텍스트

## 1. 프로젝트 목적

News-Fear-and-Greed-index는 뉴스 기사 데이터를 분석하여 종목별 뉴스 공포·탐욕 지수를 계산하고, 이를 Spring Boot 웹사이트에서 조회할 수 있게 만드는 프로젝트다.

기존 UGRP 프로젝트에서는 Python으로 네이버 뉴스 기사를 크롤링하고, KoNLPy/Okt 기반 토큰화와 긍부정 단어 분석, Dense 신경망 기반 감성 분석을 통해 날짜별 감성 점수를 계산했다.

이번 프로젝트의 목표는 기존 Python 분석 코드를 웹서비스로 확장하는 것이다.

## 2. 기존 Python 분석 흐름

기존 코드는 대략 다음 흐름을 가진다.

1. 분석 대상 키워드 설정
   - 예: 비트코인, 삼성전자, 코스피, 이노진, 한국주강

2. 날짜 범위 생성
   - 특정 기간의 날짜 리스트를 만든다.

3. 네이버 뉴스 크롤링
   - 키워드별, 날짜별 뉴스 기사를 수집한다.
   - 기사 제목, 언론사, 본문 또는 요약, URL 등을 저장한다.

4. 감성 분석
   - KoNLPy/Okt로 문장을 토큰화한다.
   - 긍정 단어와 부정 단어를 비교한다.
   - Dense 신경망 또는 감성 점수 계산 로직으로 0~1 사이 점수를 만든다.

5. 날짜별 평균 계산
   - 하루 기사들의 감성 점수 평균을 계산한다.
   - 이 값을 뉴스 공포·탐욕 지수로 변환한다.

6. 기존에는 결과를 Excel 파일로 저장했다.
   - 이번 프로젝트에서는 Excel 저장 대신 MySQL DB에 저장하는 구조로 바꾼다.

## 3. 새 웹서비스 목표

Python은 분석 엔진 역할을 한다.  
Spring Boot는 웹서비스/API 서버 역할을 한다.  
MySQL은 분석 결과 저장소 역할을 한다.

전체 구조:

```text
Python 분석 코드
→ MySQL에 기사/감성지수 저장
→ Spring Boot가 DB 조회
→ 웹 화면에서 종목별 뉴스공탐지수와 기사 목록 표시
```

## 4. 기술 스택

- Java 17
- Spring Boot
- Spring Web
- Spring Data JPA
- MySQL
- Thymeleaf
- Chart.js
- Python
- KoNLPy/Okt
- pandas

처음 MVP에서는 React, Docker, AWS, Spring Security, 로그인 기능을 넣지 않는다.

## 5. MVP 범위

처음에는 아래 3개 테이블만 사용한다.

1. assets
   - 분석 대상 종목/자산 정보

2. news_articles
   - 크롤링한 뉴스 기사와 기사별 감성 분석 결과

3. daily_news_index
   - 날짜별 종목별 뉴스 공포·탐욕 지수

## 6. MVP 화면

1. 메인 페이지
   - 분석 대상 종목 목록 표시
   - 각 종목의 최신 뉴스공탐지수 표시

2. 종목 상세 페이지
   - 종목 정보 표시
   - 날짜별 뉴스공탐지수 표 표시
   - Chart.js로 날짜별 지수 차트 표시
   - 관련 기사 목록 표시

## 7. 중요한 제약

- 처음부터 로그인 기능을 만들지 않는다.
- 처음부터 Docker를 쓰지 않는다.
- 처음부터 AWS 배포를 하지 않는다.
- 먼저 localhost에서 정상 동작하는 것을 목표로 한다.
- Python 분석 코드는 기존 코드를 최대한 재사용하되, 결과 저장 방식을 Excel에서 MySQL로 바꾸는 방향으로 진행한다.
- Spring Boot는 분석을 직접 수행하지 않고 DB에 저장된 결과를 조회하는 역할만 한다.

## 8. 원하는 구현 순서

1. 기존 Python 코드 흐름 파악
2. MySQL 테이블 설계
3. Spring Boot 프로젝트 생성
4. Entity, Repository, Service, Controller 작성
5. 샘플 데이터로 화면 출력
6. Python 결과를 MySQL에 저장하는 스크립트 작성
7. 실제 분석 결과와 웹 화면 연결
8. README 정리
9. 이후 AWS 배포는 별도 단계에서 진행
