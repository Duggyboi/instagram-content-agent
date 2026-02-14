@echo off
REM Start Instagram Content Intelligence Agent Web Interface
REM This script activates the Python environment and runs the Streamlit app

echo Activating Python environment...
call C:\Users\Keagan\anaconda3\envs\pm-agent\Scripts\activate.bat

echo.
echo Starting Instagram Content Intelligence Agent Web Interface...
echo.
echo The app will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run streamlit_app.py

pause
