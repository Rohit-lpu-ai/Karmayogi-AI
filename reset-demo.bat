@echo off
REM Local demo reset: voids the assessment attempts of ALL synthetic demo accounts in the
REM "local-demo" organisation so the baseline can be taken again. Refused outside APP_ENV=local/ci.
REM Nothing is deleted: attempts and evidence are marked voided and audited (DEC-052).
REM For one account: backend\.venv\Scripts\python -m app.seed.demo_reset --org-code local-demo --email learner01@example.invalid
setlocal
cd /d "%~dp0backend"
if not exist ".venv\Scripts\python.exe" ( echo Run start-dev.bat once first. & pause & exit /b 1 )

echo This resets every synthetic demo account (results become "voided"; history is kept).
choice /C YNJ /M "Continue? Y = reset, N = cancel, J = reset and also clear job roles (replays onboarding)"
if errorlevel 3 ( set "EXTRA=--clear-job-role" & goto run )
if errorlevel 2 exit /b 0
set "EXTRA="
:run
.venv\Scripts\python -m app.seed.demo_reset --org-code local-demo --all-synthetic %EXTRA%
echo.
pause
