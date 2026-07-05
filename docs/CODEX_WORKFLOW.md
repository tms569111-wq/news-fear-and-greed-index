# Codex 작업 순서

## 원칙

Codex에게 한 번에 전체 프로젝트를 만들라고 하지 않는다.  
아래 순서대로 작은 단위로 시킨다.

## 0단계: 읽기만 시키기

사용 프롬프트:

```text
prompts/00_read_first_no_code.md
```

목표:

- Codex가 프로젝트를 이해했는지 확인한다.
- 아직 코드는 수정하지 않는다.

## 1단계: Spring Boot MVP 생성

사용 프롬프트:

```text
prompts/01_create_mvp_spring_boot.md
```

목표:

- 3개 테이블 기반 Entity/Repository/Service/Controller 생성
- Thymeleaf 화면 생성
- 샘플 데이터로 화면 표시

## 2단계: Python 결과 DB 적재

사용 프롬프트:

```text
prompts/02_import_python_results_to_mysql.md
```

목표:

- 기존 Excel/CSV 결과를 MySQL에 넣는 스크립트 작성
- 실제 KoNLPy 크롤링 코드와 완전히 통합하기 전 임시 적재부터 성공

## 3단계: 화면 개선

사용 프롬프트:

```text
prompts/03_ui_chartjs.md
```

목표:

- 차트와 표를 보기 좋게 정리
- README용 캡처 가능한 수준으로 개선

## 4단계: 코드 설명/리팩토링

사용 프롬프트:

```text
prompts/04_refactor_and_explain.md
```

목표:

- 면접에서 설명할 수 있도록 코드 구조 설명
- 불필요한 복잡성 제거

## 5단계: 배포 문서만 작성

사용 프롬프트:

```text
prompts/05_later_ec2_deploy_readme.md
```

목표:

- 실제 AWS 배포는 나중에 하되, 배포 계획 문서 작성
