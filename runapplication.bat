```bat
@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo Vocabulary Trainer - Application Launcher
echo ==========================================
echo.

if not exist "env\Scripts\python.exe" (
    echo ERROR: Python environment not found.
    echo Please run setupdev.bat first.
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo ERROR: Frontend package.json was not found.
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo ERROR: Frontend dependencies not found.
    echo Please run setupdev.bat first.
    pause
    exit /b 1
)

echo Starting Vocabulary Trainer backend...
start "Vocabulary Trainer Backend" cmd /k "cd /d ""%~dp0"" && call env\Scripts\activate.bat && python -m uvicorn main:app --reload"

timeout /t 3 /nobreak >nul

echo Starting Vocabulary Trainer frontend...
start "Vocabulary Trainer Frontend" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"

echo.
echo ==========================================
echo Startup commands have been launched.
echo ==========================================
echo.
echo Backend API: http://127.0.0.1:8000
echo API documentation: http://127.0.0.1:8000/docs
echo Frontend: Open the URL displayed in the frontend terminal.
echo The frontend may use port 5173 or 5174.
echo.
pause
