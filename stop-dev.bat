@echo off
REM Stops whatever holds the local backend and frontend ports (after confirmation).
REM The database container keeps running; stop it with:
REM   docker compose --env-file .env -f deploy/docker-compose.yml stop db
setlocal
cd /d "%~dp0"
if not defined BACKEND_PORT set "BACKEND_PORT=8000"
set "PORTCHECK=powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy\local\dev-port.ps1""

echo Processes on port %BACKEND_PORT% (backend) and 5173 (frontend):
%PORTCHECK% -Port %BACKEND_PORT% -Kind backend
if errorlevel 1 (set "BUSY_API=1") else (echo   port %BACKEND_PORT%: free)
%PORTCHECK% -Port 5173 -Kind frontend
if errorlevel 1 (set "BUSY_WEB=1") else (echo   port 5173: free)
if not defined BUSY_API if not defined BUSY_WEB ( echo Nothing to stop. & timeout /t 5 & exit /b 0 )

choice /M "Stop the backend and frontend processes on these ports"
if errorlevel 2 exit /b 0
if defined BUSY_API %PORTCHECK% -Port %BACKEND_PORT% -Kind backend -Stop -IncludeOwn -Force
if defined BUSY_WEB %PORTCHECK% -Port 5173 -Kind frontend -Stop -IncludeOwn -Force
timeout /t 5
exit /b 0
