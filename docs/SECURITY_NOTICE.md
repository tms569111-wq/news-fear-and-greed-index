# 보안/개인정보 주의

## 이 패키지에 포함하지 않은 파일

- 비번.txt
- 개인정보가 들어간 원본 보고서
- HWP 양식 원본

## GitHub에 올리면 안 되는 것

- DB 비밀번호
- AWS Access Key
- 개인 전화번호
- 개인 이메일
- 학번
- `.env`
- `application-secret.yml`
- `비번.txt`
- 원본 개인정보 보고서

## application.yml 관리 원칙

DB 계정은 처음에는 로컬 테스트용으로만 사용한다.

나중에 배포할 때는 다음처럼 환경변수로 분리한다.

```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
```

## .gitignore 필수 패턴

```text
.env
*.secret
*password*
*비번*
application-secret.yml
```
