
@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo Vocabulary Trainer - Development Setup
echo ==========================================

if not exist "env\Scripts\python.exe" (
    echo Creating Python virtual environment...
    python -m venv env
    if errorlevel 1 goto error
)

echo Activating virtual environment...
call env\Scripts\activate.bat

echo Installing Python dependencies...
python -m pip install --upgrade pip
if errorlevel 1 goto error

python -m pip install -r requirements.txt
if errorlevel 1 goto error

echo.
echo Installing frontend dependencies...
if exist "frontend\package.json" (
    cd frontend
    call npm install
    if errorlevel 1 goto error
    cd ..
) else (
    echo WARNING: frontend\package.json was not found.
)

echo.
echo Setup completed successfully!
echo Run runapplication.bat to start the application.
pause
exit /b 0

:error
echo.
echo ERROR: Setup failed. Check the messages above.
pause
exit /b 1
