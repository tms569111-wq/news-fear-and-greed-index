# 3일 localhost MVP 실행 체크리스트

## 완료 기준

아래 네 가지가 모두 되면 1차 MVP 완료입니다.

- `localhost:8080`에서 종목 목록과 최신 지수가 보인다.
- 종목 상세 화면에서 날짜별 차트와 기사 목록이 보인다.
- Python을 실행하면 전날 뉴스 CSV가 생성된다.
- 적재기를 실행한 뒤 새로고침하면 DB의 새 날짜 데이터가 보인다.

## Day 1 — DB와 Spring 화면 관통

- [ ] MySQL 8 실행
- [ ] `db/schema_mvp.sql` 실행
- [ ] `db/seed_sample.sql` 실행
- [ ] `spring-app/src/main/resources/application.properties`의 DB 사용자 확인
- [ ] 환경변수 `DB_PASSWORD` 설정
- [ ] `spring-app/gradlew.bat bootRun`
- [ ] `/`, `/assets/1`, `/api/assets/1/index` 확인

막히면 순서대로 확인합니다.

1. MySQL 서비스가 실행 중인가?
2. `news_fear_greed` DB가 있는가?
3. root 비밀번호가 `DB_PASSWORD`와 같은가?
4. 콘솔의 첫 번째 `Caused by`는 무엇인가?

## Day 2 — 실제 Python 결과 연결

- [ ] 루트 `.venv` 생성 후 `requirements-local.txt` 설치
- [ ] `python-pipeline/.env`에 네이버 ID/Secret 입력
- [ ] 처음에는 삼성전자 한 종목, 특정 날짜로 실행

```bash
python python-pipeline/run_daily_pipeline.py --date 2026-07-10 --asset-code 005930
```

- [ ] `python-pipeline/output`의 CSV 두 개 직접 열어 값 확인
- [ ] `python-import/.env`에 MySQL 접속 정보 입력
- [ ] 적재기 실행

```bash
python python-import/import_pipeline_csv_to_mysql.py
```

- [ ] MySQL에서 행 수 확인

```sql
SELECT COUNT(*) FROM news_articles;
SELECT * FROM daily_news_index ORDER BY target_date DESC;
```

- [ ] Spring 상세 화면 새로고침

## Day 3 — 재실행·예외·예약

- [ ] 같은 날짜를 두 번 실행해 지수가 중복되지 않는지 확인
- [ ] 잘못된 DB 비밀번호에서 적재기가 롤백되는지 확인
- [ ] 데이터가 없는 활성 종목이 `NO_DATA`로 보이는지 확인
- [ ] `scripts/run_daily_local.bat`을 수동으로 실행
- [ ] Windows 작업 스케줄러에 매일 09:00 등록
- [ ] README 실행 명령이 본인 PC 경로에서 그대로 되는지 최종 확인

## 지금 당장 하지 않을 것

- Spring에서 Python 프로세스 실행
- 브라우저 버튼으로 실시간 크롤링
- React 분리
- Docker/AWS 배포
- 딥러닝 모델 재학습 자동화

지금은 짧고 확실한 배치 경로 하나를 완성한 다음, 실제 데이터 분포를 확보해
감성 분석 정확도를 개선합니다.
