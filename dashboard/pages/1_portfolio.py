import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sqlite3

def init_db():
    conn = sqlite3.connect('stock_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (timestamp TEXT, stock TEXT, action TEXT, quantity INTEGER, price REAL)''')
    conn.commit()
    return conn

def main():
    st.title("📊 Portfolio Analysis")
    
    conn = init_db()
    
    # Portfolio Summary
    st.subheader("Current Holdings")
    
    # Sample portfolio data (replace with actual DB query)
    holdings = pd.DataFrame({
        'Stock': ['RELIANCE', 'TCS', 'INFY'],
        'Quantity': [10, 5, 8],
        'Current Price': [2500, 3500, 1500],
        'Total Value': [25000, 17500, 12000]
    })
    
    st.dataframe(holdings)
    
    # Portfolio Distribution Pie Chart
    fig = px.pie(holdings, values='Total Value', names='Stock', title='Portfolio Distribution')
    st.plotly_chart(fig)
    
    # Transaction Form
    st.subheader("Make Transaction")
    col1, col2, col3 = st.columns(3)
    with col1:
        stock = st.selectbox("Select Stock", holdings['Stock'])
    with col2:
        action = st.selectbox("Action", ["Buy", "Sell"])
    with col3:
        quantity = st.number_input("Quantity", min_value=1)
        
    if st.button("Execute Transaction"):
        # Add transaction to database
        c = conn.cursor()
        c.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)",
                 (datetime.now().isoformat(), stock, action, quantity, holdings[holdings['Stock']==stock]['Current Price'].values[0]))
        conn.commit()
        st.success(f"{action} order executed for {quantity} shares of {stock}")

if __name__ == "__main__":
    main()
