@echo off
echo Installing Python requirements...
python -m pip install --upgrade pip
python -m pip install streamlit pandas plotly numpy python-dotenv

echo Setting up environment...
mkdir data 2>nul
echo Installation complete!
pause
