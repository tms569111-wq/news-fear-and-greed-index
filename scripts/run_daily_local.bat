@echo off
setlocal

set "PROJECT_ROOT=%~dp0.."
set "PYTHON=%PROJECT_ROOT%\.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
  echo [ERROR] .venv가 없습니다. README의 처음 한 번 설치를 먼저 실행하세요.
  exit /b 1
)

echo [1/2] 전날 뉴스 CSV를 생성합니다.
"%PYTHON%" "%PROJECT_ROOT%\python-pipeline\run_daily_pipeline.py"
if errorlevel 1 exit /b 1

echo [2/2] CSV를 MySQL에 적재합니다.
"%PYTHON%" "%PROJECT_ROOT%\python-import\import_pipeline_csv_to_mysql.py"
if errorlevel 1 exit /b 1

echo 뉴스공탐지수 일일 작업이 완료되었습니다.
endlocal
