@echo off
SETLOCAL

REM 프로젝트 루트로 이동
cd /d %~dp0

REM 가상환경이 없으면 생성
IF NOT EXIST ".venv" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
)

REM 가상환경 활성화
call .\.venv\Scripts\activate

REM 패키지 설치
IF EXIST "requirements.txt" (
    echo [INFO] Installing requirements...
    pip install -r requirements.txt
)

REM 프로그램 실행
echo [INFO] Starting pilot...
python run.py

echo.
echo [INFO] Finished. Press any key to exit.
pause
ENDLOCAL
