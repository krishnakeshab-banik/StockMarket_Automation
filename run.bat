@echo off
echo Installing requirements...
pip install -r requirements.txt

echo Starting AI Stock Dashboard...
cd dashboard
streamlit run dashboard.py
