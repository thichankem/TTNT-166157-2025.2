@echo off
setlocal
rem ====== Chay backend FastAPI (cong 8000) ======
cd /d "%~dp0backend"
set "PYTHONUTF8=1"

rem Python co day du thu vien (anaconda). Neu khong co thi fallback sang 'python'.
set "PY=C:\Users\ADMIN\anaconda3\python.exe"
if not exist "%PY%" set "PY=python"

"%PY%" -c "import fastapi, uvicorn, sklearn, pandas, numpy" 2>nul
if errorlevel 1 (
  echo [LOI] Python tai "%PY%" thieu thu vien.
  echo Hay cai dat: "%PY%" -m pip install -r requirements.txt
  pause
  exit /b 1
)

echo ============================================
echo  Backend dang chay: http://127.0.0.1:8000
echo  Nhan Ctrl+C de dung.
echo ============================================
"%PY%" main.py
pause
