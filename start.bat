@echo off
setlocal enabledelayedexpansion

title LLM Council Launcher

echo ===================================================
echo               LLM Council Launcher
echo ===================================================
echo.

:: Step 1: Pre-flight checks
echo [*] Checking dependencies...

where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] WARNING: 'uv' is not installed or not in PATH.
    echo [*] Checking Python fallback...
    where python >nul 2>&1
    if %errorlevel% neq 0 (
        set "ERR_MSG=Neither 'uv' nor 'python' was found in PATH."
        goto :error
    )
    set "RUN_CMD=python -m backend.main"
) else (
    set "RUN_CMD=uv run python -m backend.main"
)

where npm >nul 2>&1
if %errorlevel% neq 0 (
    set "ERR_MSG='npm' is not installed or not in PATH."
    goto :error
)

:: Check for .env file
if not exist ".env" (
    echo [!] WARNING: .env file not found. Copying .env.example if available...
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [*] Created .env from .env.example
    ) else (
        echo [!] WARNING: No .env file present. Please ensure API keys are set.
    )
)

:: Step 2: Install frontend node_modules if missing
if not exist "frontend\node_modules" (
    echo [*] Installing frontend dependencies...
    cd frontend
    call npm install
    if %errorlevel% neq 0 (
        cd ..
        set "ERR_MSG=Failed to install frontend dependencies."
        goto :error
    )
    cd ..
)

:: Step 3: Start Services
echo.
echo [*] Starting Backend Service on http://localhost:8001...
start "LLM Council - Backend" /B %RUN_CMD%
if %errorlevel% neq 0 (
    set "ERR_MSG=Failed to start backend service."
    goto :error
)

echo [*] Starting Frontend Service on http://localhost:5173...
cd frontend
start "LLM Council - Frontend" /B npm run dev
if %errorlevel% neq 0 (
    cd ..
    set "ERR_MSG=Failed to start frontend service."
    goto :error
)
cd ..

echo.
echo ===================================================
echo  [✓] LLM Council is running successfully!
echo      Backend:  http://localhost:8001
echo      Frontend: http://localhost:5173
echo ===================================================
echo.
echo Press any key to terminate servers...
pause >nul

:: Cleanup background tasks on press
echo [*] Shutting down services...
taskkill /FI "WINDOWTITLE eq LLM Council - Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq LLM Council - Frontend*" /F >nul 2>&1
echo [✓] Shutdown complete.
exit /b 0

:error
echo.
echo ===================================================
echo  [X] ERROR: %ERR_MSG%
echo ===================================================
echo.
pause
exit /b 1
