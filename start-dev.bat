@echo off
REM ---------------------------------------------------------------------------
REM  Competency Learning Platform - local launcher
REM  database (5433) -> backend (BACKEND_PORT, default 8000) -> frontend (5173)
REM  Double-click to start. Close the Backend / Frontend windows or run stop-dev.bat to stop.
REM ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0"
set "ROOT=%~dp0"
if not defined BACKEND_PORT set "BACKEND_PORT=8000"
set "FRONTEND_PORT=5173"
set "API_URL=http://127.0.0.1:%BACKEND_PORT%"
set "PORTCHECK=powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT%deploy\local\dev-port.ps1""

echo.
echo === [1/6] Checking Docker ===
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker is not running. Trying to start Docker Desktop...
    if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" start "" "%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
    for /l %%i in (1,1,60) do (
        docker info >nul 2>&1 && goto docker_ok
        timeout /t 3 /nobreak >nul
    )
    echo ERROR: Docker did not start. Open Docker Desktop manually and run this again.
    goto fail
)
:docker_ok

echo.
echo === [2/6] Starting PostgreSQL (127.0.0.1:5433) ===
if not exist ".env" (
    echo ERROR: .env is missing. Copy .env.example to .env and fill it in.
    goto fail
)
docker compose --env-file .env -f deploy/docker-compose.yml up -d db
if errorlevel 1 ( echo ERROR: could not start the database container. & goto fail )
set "DBSTATE="
for /l %%i in (1,1,40) do (
    for /f %%s in ('docker inspect -f "{{.State.Health.Status}}" platform-local-db-1 2^>nul') do set "DBSTATE=%%s"
    call :is_healthy && goto db_ok
    timeout /t 2 /nobreak >nul
)
echo ERROR: database did not become healthy. Check: docker logs platform-local-db-1
goto fail
:db_ok
echo Database is healthy.

echo.
echo === [3/6] Preparing backend ===
if not exist "backend\.venv\Scripts\python.exe" (
    echo Creating Python virtual environment and installing packages ^(first run only^)...
    python -m venv backend\.venv || ( echo ERROR: python not found on PATH. & goto fail )
    backend\.venv\Scripts\python -m pip install -r backend\requirements.lock || goto fail
)
pushd backend
.venv\Scripts\python -m alembic upgrade head
if errorlevel 1 ( popd & echo ERROR: database migration failed. & goto fail )
popd

echo.
echo === [4/6] Checking ports %BACKEND_PORT% and %FRONTEND_PORT% ===
set "START_BACKEND=1"
%PORTCHECK% -Port %BACKEND_PORT% -Kind backend -Stop
set "RC=%ERRORLEVEL%"
if "%RC%"=="10" ( echo Backend already running on port %BACKEND_PORT% - reusing it. & set "START_BACKEND=0" )
if "%RC%"=="22" ( echo ERROR: port %BACKEND_PORT% is busy. Stop that process, or run with another port: set BACKEND_PORT=8010 ^&^& start-dev.bat & goto fail )
set "START_FRONTEND=1"
%PORTCHECK% -Port %FRONTEND_PORT% -Kind frontend -Stop
set "RC=%ERRORLEVEL%"
if "%RC%"=="10" ( echo Frontend already running on port %FRONTEND_PORT% - reusing it. & set "START_FRONTEND=0" )
if "%RC%"=="22" ( echo ERROR: port %FRONTEND_PORT% is busy. Stop that process and run this again. & goto fail )
if "%START_FRONTEND%"=="0" if not "%BACKEND_PORT%"=="8000" (
    echo WARNING: the running frontend may proxy to a different backend port. Run stop-dev.bat, then start again.
)

echo.
echo === [5/6] Starting backend on %API_URL% ===
if "%START_BACKEND%"=="1" (
    start "Competency Learning Platform - Backend" cmd /k "cd /d "%ROOT%backend" && .venv\Scripts\python -m uvicorn --factory app.main:app_factory --host 127.0.0.1 --port %BACKEND_PORT% --reload"
)
REM Wait until this project's API answers, so the frontend never starts against a dead proxy target.
for /l %%i in (1,1,40) do (
    %PORTCHECK% -Port %BACKEND_PORT% -Kind backend >nul 2>&1
    if errorlevel 10 if not errorlevel 11 goto api_ok
    timeout /t 1 /nobreak >nul
)
echo ERROR: the backend did not start. Read the error in the Backend window.
goto fail
:api_ok
echo Backend is answering.

echo.
echo === [6/6] Starting frontend on http://localhost:%FRONTEND_PORT% (API proxy -^> %API_URL%) ===
if not exist "frontend\node_modules" (
    echo Installing frontend packages ^(first run only^)...
    pushd frontend & call npm install & popd
)
if "%START_FRONTEND%"=="1" (
    start "Competency Learning Platform - Frontend" cmd /k "cd /d "%ROOT%frontend" && set "API_PROXY_TARGET=%API_URL%" && npm run dev"
)
for /l %%i in (1,1,40) do (
    %PORTCHECK% -Port %FRONTEND_PORT% -Kind frontend >nul 2>&1
    if errorlevel 10 if not errorlevel 11 goto web_ok
    timeout /t 1 /nobreak >nul
)
echo WARNING: the frontend has not answered yet - check the Frontend window.
:web_ok
start "" http://localhost:%FRONTEND_PORT%/

echo.
echo All started.
echo   App      : http://localhost:%FRONTEND_PORT%/
echo   Backend  : %API_URL%/healthz   (API docs: %API_URL%/docs)
echo   Stop     : close the two windows, or run stop-dev.bat
echo   Demo data: see backend\README.md ("Demo packs and reset")
echo.
timeout /t 10
exit /b 0

:fail
echo.
pause
exit /b 1

:is_healthy
if /i "%DBSTATE%"=="healthy" exit /b 0
exit /b 1

