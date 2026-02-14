@echo off
REM Set up PATH to include ffmpeg from pm-agent conda environment
set PATH=C:\Users\Keagan\anaconda3\envs\pm-agent\Library\bin;C:\Users\Keagan\anaconda3\envs\pm-agent\Scripts;C:\Users\Keagan\anaconda3\envs\pm-agent;%PATH%

REM Verify ffmpeg is available
echo Checking ffmpeg availability...
where ffmpeg
if errorlevel 1 (
    echo ERROR: ffmpeg not found in PATH
    pause
    exit /b 1
)

echo ffmpeg found successfully. Starting Streamlit app...
echo.

REM Start Streamlit app
cd /d C:\Users\Keagan\projects\instagram-content-agent
C:\Users\Keagan\anaconda3\envs\pm-agent\python.exe -m streamlit run streamlit_app.py

pause
