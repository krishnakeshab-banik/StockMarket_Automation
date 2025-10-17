import subprocess
import sys
import os

def install_requirements():
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas", "plotly", "numpy"])

def run_streamlit():
    try:
        os.chdir(os.path.join(os.path.dirname(__file__), "dashboard"))
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except Exception as e:
        print(f"Error running Streamlit: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    install_requirements()
    run_streamlit()
