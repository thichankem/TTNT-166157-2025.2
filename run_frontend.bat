@echo off
setlocal
rem ====== Chay frontend Vite + React (cong 5173) ======
cd /d "%~dp0frontend"

if not exist node_modules (
  echo Dang cai dat thu vien npm lan dau...
  call npm install
)

echo ============================================
echo  Frontend dang chay: http://localhost:5173
echo  Nhan Ctrl+C de dung.
echo ============================================
call npm run dev
pause
