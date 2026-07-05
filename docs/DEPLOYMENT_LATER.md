# 배포는 나중 단계

## 지금은 배포하지 않는다

1차 MVP 목표는 localhost 실행이다.

```text
http://localhost:8080
```

여기서 화면이 정상적으로 떠야 한다.

## 나중 배포 목표

처음 배포는 복잡하게 하지 않는다.

```text
AWS EC2 1대
- Spring Boot jar 실행
- MySQL 설치
- Python script 수동 실행 또는 cron 실행
```

## 배포 전 체크리스트

- 로컬에서 `./gradlew bootRun` 또는 `java -jar` 실행 성공
- MySQL 접속 성공
- 샘플 데이터 조회 성공
- `/` 화면 접속 성공
- `/assets/{id}` 화면 접속 성공
- README에 로컬 실행 방법 작성 완료

## 나중에 추가할 수 있는 것

- Docker Compose
- RDS
- Nginx
- HTTPS
- 도메인
- GitHub Actions

그러나 지금은 전부 제외한다.
