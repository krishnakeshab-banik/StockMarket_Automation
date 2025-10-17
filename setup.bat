@echo off
echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing required packages...
python -m pip install --upgrade pip
pip install streamlit pandas plotly numpy python-dotenv

echo Setup complete! Run start.bat to launch the dashboard.
pause
