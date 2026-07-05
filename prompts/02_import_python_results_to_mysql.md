Python 분석 결과를 MySQL에 넣는 최소 스크립트를 작성해주세요.

목표:

- 기존에는 Excel/CSV로 저장하던 분석 결과를 MySQL에 저장하는 구조로 바꿉니다.
- 먼저 완전한 크롤러 통합이 아니라, 샘플 Excel/CSV 또는 DataFrame을 읽어서 DB에 insert하는 형태로 구현합니다.

요구사항:

1. `python-import` 폴더에 스크립트 작성
2. pandas로 Excel/CSV 읽기
3. pymysql 또는 mysql-connector-python 중 하나 사용
4. assets, news_articles, daily_news_index 테이블에 데이터를 넣는 함수 작성
5. DB 접속 정보는 코드에 직접 박지 말고 `.env.example`을 참고하게 작성
6. README에 실행 방법 작성

주의:
- 실제 비밀번호를 코드에 넣지 마세요.
- 크롤링 자동화는 아직 하지 마세요.
- 먼저 기존 결과 파일을 DB에 넣는 것만 성공시키세요.
