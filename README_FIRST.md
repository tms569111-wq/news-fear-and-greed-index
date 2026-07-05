# News-Fear-and-Greed-index Codex 인수인계 패키지

이 zip은 `D:\project`에 압축을 풀어서 Codex에게 그대로 읽히기 위한 **프로젝트 맥락/명세/프롬프트 패키지**입니다.

권장 위치:

```text
D:\project\News-Fear-and-Greed-index\
```

## 먼저 할 일

1. 이 폴더 전체를 VS Code 또는 Codex 작업공간으로 엽니다.
2. Codex에게 바로 코드를 만들라고 하지 말고, 먼저 `prompts/00_read_first_no_code.md` 내용을 그대로 붙여 넣습니다.
3. Codex가 프로젝트를 제대로 이해했는지 확인합니다.
4. 이해가 맞으면 `prompts/01_create_mvp_spring_boot.md`를 붙여 넣어 1차 MVP만 만들게 합니다.

## 이 패키지의 목적

기존 UGRP Python 뉴스 감성 분석 프로젝트를 Spring Boot 웹서비스로 확장합니다.

핵심 구조:

```text
Python 분석 코드
→ MySQL에 기사/감성지수 저장
→ Spring Boot가 DB 조회
→ Thymeleaf/Chart.js 웹 화면에서 뉴스공탐지수 표시
```

## 지금 단계에서 절대 넣지 말 것

- React
- Docker
- AWS 배포
- RDS
- Nginx
- HTTPS
- Spring Security
- 로그인/회원가입
- 실시간 크롤링 API

처음 목표는 **localhost에서 종목 목록, 종목 상세, 날짜별 뉴스공탐지수 차트가 보이는 것**입니다.

## 포함한 기존 자료

- `legacy/code/`: 기존 Python 노트북
- `legacy/data/`: 기존 Excel 결과 파일
- `legacy/report/`: 개인정보를 줄인 블라인드 보고서
- `docs/`: Codex가 읽어야 하는 명세 문서
- `prompts/`: Codex에게 순서대로 던질 프롬프트
- `db/`: MySQL 테이블 설계와 샘플 데이터
- `data/sample/`: CSV 샘플 데이터

## 보안 주의

`비번.txt`, 개인정보가 들어간 원본 보고서, HWP 양식은 이 패키지에 넣지 않았습니다.
GitHub에 올릴 때도 절대 비밀번호/개인정보/DB 계정 파일을 올리지 마세요.
