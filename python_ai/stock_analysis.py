import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Choose companies
companies = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']

# Step 2: Define the absolute path to the data folder
data_folder = r"C:\Users\godre\Desktop\AI_Stock_Automation\data"

# Step 3: Make sure the folder exists
os.makedirs(data_folder, exist_ok=True)

# Step 4: Fetch and save data
for company in companies:
    data = yf.download(company, period="6mo", interval="1d")
    file_path = os.path.join(data_folder, f"{company}_data.csv")
    data.to_csv(file_path)
    print(f"\n✅ Saved data for {company} at {file_path}")

    # Plot closing price trend
    plt.figure(figsize=(8, 4))
    plt.plot(data['Close'], label=f'{company} Close Price')
    plt.title(f'{company} Stock Trend (6 months)')
    plt.xlabel('Date')
    plt.ylabel('Price (₹)')
    plt.legend()
    plt.show()
