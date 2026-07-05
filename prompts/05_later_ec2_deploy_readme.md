아직 실제 배포는 하지 않고, EC2 단일 서버 배포 문서만 작성해주세요.

목표:

- 나중에 AWS EC2 Ubuntu 서버에 Spring Boot jar + MySQL을 올릴 때 따라할 수 있는 문서를 만듭니다.

작성할 문서:

`docs/EC2_DEPLOYMENT_GUIDE.md`

포함 내용:

1. EC2 인스턴스 생성 시 주의사항
2. 보안그룹에서 22, 8080 포트 열기
3. Java 17 설치
4. MySQL 설치
5. DB와 사용자 생성
6. Spring Boot jar 빌드
7. jar 업로드
8. 서버에서 실행
9. 로그 확인
10. 서버 중지 방법
11. 비용 관리 주의사항

제외:
- RDS
- Docker
- Nginx
- HTTPS
- 도메인 연결
