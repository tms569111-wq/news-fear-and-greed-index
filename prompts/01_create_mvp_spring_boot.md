이제 1단계 MVP를 구현해주세요.

요구사항:

- Java 17
- Spring Boot
- Spring Web
- Spring Data JPA
- MySQL
- Thymeleaf
- Chart.js
- Gradle 또는 Maven 중 프로젝트에 맞는 하나 선택

구현 범위:

1. `spring-app` 폴더에 Spring Boot 프로젝트 생성 또는 기존 프로젝트가 있으면 그 안에 구현
2. assets, news_articles, daily_news_index에 해당하는 JPA Entity 작성
3. Repository 작성
4. Service 작성
5. Controller 작성
6. 메인 페이지 작성
   - 종목 목록 표시
   - 각 종목의 최신 뉴스공탐지수 표시
7. 종목 상세 페이지 작성
   - 종목 정보 표시
   - 날짜별 뉴스공탐지수 표 표시
   - Chart.js 차트 표시
   - 기사 목록 표시
8. data.sql 또는 import.sql로 샘플 데이터 추가
9. README에 로컬 실행 방법 작성

제외:
- 로그인
- 회원가입
- Spring Security
- Docker
- AWS
- RDS
- Python 자동 실행

중요:
- 너무 복잡하게 만들지 마세요.
- 신입 개발자가 이해할 수 있는 단순한 Controller-Service-Repository 구조로 작성해주세요.
- 실행 가능한 상태를 우선해주세요.
