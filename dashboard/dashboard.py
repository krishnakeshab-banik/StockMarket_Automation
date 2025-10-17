# NOTE: This Streamlit dashboard is a prototype.
# The production platform should use a React.js frontend and FastAPI backend as described in the architecture plan.

import streamlit as st
from utils.local_llm import LocalStockAdvisor
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import sqlite3

# Ensure proper path handling
import sys
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

st.set_page_config(page_title="AI Stock Dashboard", layout="wide")
st.title("📈 AI Stock Market Dashboard")

# Paths
json_path = parent_dir / "data" / "real_time_sentiment.json"

# Create directories if they don't exist
data_dir = parent_dir / "data"
data_dir.mkdir(exist_ok=True)

# Check if JSON exists with better error handling
try:
    if not json_path.exists():
        # Create sample data if file doesn't exist
        sample_data = {
            "RELIANCE": {
                "average_sentiment": 0.75,
                "action": "Buy",
                "headlines": ["Sample headline 1", "Sample headline 2"]
            }
        }
        json_path.write_text(json.dumps(sample_data, indent=4))
    
    with open(json_path, "r") as f:
        data = json.load(f)
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    data = {}

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'llm_initialized' not in st.session_state:
    st.session_state.llm_initialized = False

# Initialize LLM with error handling
@st.cache_resource
def init_llm():
    try:
        llm = LocalStockAdvisor()
        st.session_state.llm_initialized = True
        return llm
    except Exception as e:
        st.error(f"Failed to initialize AI Advisor: {str(e)}")
        return None

llm = init_llm()

# Initialize SQLite database
def init_db():
    try:
        conn = sqlite3.connect('stock_data.db', check_same_thread=False)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (timestamp TEXT, stock TEXT, action TEXT, quantity INTEGER, price REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS portfolio
                     (stock TEXT PRIMARY KEY, quantity INTEGER, avg_price REAL)''')
        conn.commit()
        return conn
    except Exception as e:
        st.error(f"Database initialization failed: {str(e)}")
        return None

conn = init_db()

# Sidebar for wallet info (optional)
wallet_balance = st.sidebar.empty()
investments_table = st.sidebar.empty()
trading_status = st.sidebar.empty()
trading_status.success("🟢 AI Trading System Active")

# Process data
companies = []
average_sentiments = []
actions = []
headlines_all = []

st.subheader("📊 Company Sentiments & Actions")
for company, details in data.items():
    companies.append(company)
    avg_sent = details.get("average_sentiment", 0)
    action = details.get("action", "Hold")
    headlines = details.get("headlines", [])

    average_sentiments.append(avg_sent)
    actions.append(action)
    headlines_all.append(headlines)

    st.markdown(f"### {company}")
    st.markdown(f"**Average Sentiment:** {avg_sent}")
    st.markdown(f"**AI Action:** {action}")
    st.markdown("**Headlines:**")
    for h in headlines:
        st.markdown(f"- {h}")
    st.markdown("---")

# Simulate investments bar chart
st.subheader("💰 Investments Overview")
investments = {company: 1000 * avg_sent + 1000 for company, avg_sent in zip(companies, average_sentiments)}
total_invested = sum(investments.values())
wallet_balance_value = 5000 - total_invested

# Update sidebar
wallet_balance.metric("Wallet Balance", f"₹{wallet_balance_value:.2f}")
investments_df = pd.DataFrame(list(investments.items()), columns=["Company", "Invested Amount"])
investments_table.dataframe(investments_df)

# Replace matplotlib with Plotly for interactive charts
fig = go.Figure(data=[
    go.Bar(name='Investments', x=list(investments.keys()), y=list(investments.values()))
])
fig.update_layout(title='Investments per Company', yaxis_title='Investment (₹)')
st.plotly_chart(fig)

# Add price trends (dummy data for demonstration)
st.subheader("📈 Price Trends")
dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
for company in companies:
    price_data = pd.DataFrame({
        'Date': dates,
        'Price': [100 + i + np.random.normal(0, 2) for i in range(30)]
    })
    fig = px.line(price_data, x='Date', y='Price', title=f'{company} Price Trend')
    st.plotly_chart(fig)

# Add quick actions
def safe_switch_page(page_path):
    try:
        st.switch_page(page_path)
    except Exception as e:
        st.error(f"Error navigating to page: {str(e)}")
        st.info(f"Make sure all pages exist in the pages directory")

st.subheader("⚡ Quick Actions")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("View Portfolio"):
        safe_switch_page("pages/1_portfolio.py")
with col2:
    if st.button("Check News"):
        safe_switch_page("pages/2_news.py")
with col3:
    if st.button("Ask AI Advisor"):
        safe_switch_page("pages/3_chatbot.py")
with col4:
    if st.button("Transaction Portal"):
        safe_switch_page("pages/4_transactions.py")

# Combined Company Section with Trading
st.subheader("📊 Company Analysis & Trading")
for company, details in data.items():
    with st.expander(f"{company} - Analysis & Trading"):
        col1, col2 = st.columns([2,1])
        
        with col1:
            st.markdown(f"**Average Sentiment:** {details.get('average_sentiment', 0):.2f}")
            st.markdown(f"**AI Action:** {details.get('action', 'Hold')}")
            st.markdown("**Recent Headlines:**")
            for h in details.get('headlines', [])[:3]:  # Show only top 3 headlines
                st.markdown(f"- {h}")
        
        with col2:
            try:
                quantity = st.number_input(f"Quantity ({company})", 
                                         min_value=1, 
                                         max_value=100,
                                         value=1)
                
                col3, col4 = st.columns(2)
                with col3:
                    if st.button(f"Buy {company}", key=f"buy_{company}"):
                        if conn:
                            try:
                                # Add loading animation
                                with st.spinner(f"Processing buy order for {company}..."):
                                    c = conn.cursor()
                                    price = investments[company]/1000
                                    c.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)",
                                            (datetime.now().isoformat(), company, "BUY", 
                                             quantity, price))
                                
                                    # Update portfolio
                                    c.execute("""INSERT OR REPLACE INTO portfolio 
                                              VALUES (?, ?, ?)""", 
                                              (company, quantity, price))
                                    conn.commit()
                                    st.success(f"Bought {quantity} shares of {company}")
                                    st.session_state.transactions.append({
                                        'time': datetime.now(),
                                        'action': 'BUY',
                                        'company': company,
                                        'quantity': quantity,
                                        'price': price
                                    })
                                    st.balloons()  # Add visual feedback
                            except Exception as e:
                                st.error(f"Transaction failed: {str(e)}")
                
                with col4:
                    if st.button(f"Sell {company}", key=f"sell_{company}"):
                        if conn:
                            try:
                                # Check if user has enough shares
                                c = conn.cursor()
                                c.execute("SELECT quantity FROM portfolio WHERE stock=?", 
                                        (company,))
                                result = c.fetchone()
                                if result and result[0] >= quantity:
                                    price = investments[company]/1000
                                    c.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)",
                                            (datetime.now().isoformat(), company, "SELL", 
                                             quantity, price))
                                    
                                    # Update portfolio
                                    new_quantity = result[0] - quantity
                                    if new_quantity > 0:
                                        c.execute("""UPDATE portfolio 
                                                       SET quantity=? WHERE stock=?""",
                                                       (new_quantity, company))
                                    else:
                                        c.execute("DELETE FROM portfolio WHERE stock=?",
                                                (company,))
                                    conn.commit()
                                    st.success(f"Sold {quantity} shares of {company}")
                                else:
                                    st.error("Not enough shares to sell")
                            except Exception as e:
                                st.error(f"Transaction failed: {str(e)}")
            except Exception as e:
                st.error(f"Trading interface error: {str(e)}")

# AI Chat Interface with error handling
st.sidebar.subheader("💬 AI Advisor")
if st.session_state.llm_initialized:
    user_question = st.sidebar.text_input("Ask about stocks...")
    if user_question:
        try:
            context = f"Portfolio: {investments}\nMarket Sentiment: {average_sentiments}"
            response = llm.get_response(user_question, context)
            st.sidebar.write("AI Response:", response)
        except Exception as e:
            st.sidebar.error(f"AI Advisor error: {str(e)}")
else:
    st.sidebar.warning("AI Advisor is not available")
