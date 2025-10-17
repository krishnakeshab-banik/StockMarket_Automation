@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting AI Stock Dashboard...
cd dashboard
streamlit run dashboard.py
pause
