@echo off
REM Instagram Content Intelligence Agent - Development Helper
REM This script provides quick commands for common development tasks

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo   Instagram Content Intelligence Agent
echo   Development Helper
echo ====================================================
echo.
echo Available commands:
echo   1. Start Streamlit app
echo   2. Verify setup
echo   3. Install dependencies
echo   4. Run tests
echo   5. Clean temporary files
echo   6. Open results folder
echo   7. View logs
echo   8. Exit
echo.

:menu
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto start_app
if "%choice%"=="2" goto verify
if "%choice%"=="3" goto install
if "%choice%"=="4" goto tests
if "%choice%"=="5" goto clean
if "%choice%"=="6" goto results
if "%choice%"=="7" goto logs
if "%choice%"=="8" goto exit_script
if "%choice%"=="exit" goto exit_script

echo Invalid choice. Please try again.
goto menu

:start_app
echo.
echo Starting Streamlit app...
call C:\Users\Keagan\anaconda3\envs\pm-agent\Scripts\activate.bat
streamlit run streamlit_app.py
goto end

:verify
echo.
echo Running setup verification...
call C:\Users\Keagan\anaconda3\envs\pm-agent\Scripts\activate.bat
python verify_setup.py
goto end

:install
echo.
echo Installing dependencies...
call C:\Users\Keagan\anaconda3\envs\pm-agent\Scripts\activate.bat
pip install -r requirements.txt
goto end

:tests
echo.
echo Running tests...
call C:\Users\Keagan\anaconda3\envs\pm-agent\Scripts\activate.bat
if exist tests (
    pytest tests/ -v
) else (
    echo No tests directory found.
)
goto end

:clean
echo.
echo Cleaning temporary files...
if exist temp_uploads (
    rd /s /q temp_uploads
    mkdir temp_uploads
    echo Cleaned temp_uploads/
)
if exist __pycache__ (
    rd /s /q __pycache__
    echo Cleaned __pycache__/
)
echo Cleanup complete.
goto end

:results
echo.
echo Opening results folder...
if not exist results (
    mkdir results
)
start "" results
goto end

:logs
echo.
echo Opening logs folder...
if not exist logs (
    mkdir logs
)
start "" logs
goto end

:exit_script
echo Goodbye!
exit /b 0

:end
echo.
pause
goto menu
