import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime, timedelta
import random

def generate_demo_transactions(conn, companies):
    """Generate demo transactions if none exist"""
    c = conn.cursor()
    # Clear existing transactions for demo
    c.execute("DELETE FROM transactions")
    c.execute("DELETE FROM portfolio")
    
    # Generate last 7 days of transactions
    for i in range(7):
        transaction_date = datetime.now() - timedelta(days=i)
        for company in companies:
            # Random buy/sell with 70% buy probability
            action = "BUY" if random.random() < 0.7 else "SELL"
            quantity = random.randint(5, 20)
            price = random.uniform(800, 1200)
            
            c.execute("""INSERT INTO transactions 
                        VALUES (?, ?, ?, ?, ?)""",
                     (transaction_date.isoformat(), company, action, 
                      quantity, price))
            
            # Update portfolio
            if action == "BUY":
                c.execute("""INSERT OR REPLACE INTO portfolio 
                            VALUES (?, ?, ?)""", 
                         (company, quantity, price))
    conn.commit()

def load_transactions():
    try:
        conn = sqlite3.connect('stock_data.db', check_same_thread=False)
        c = conn.cursor()
        
        # Check if we have any transactions
        c.execute("SELECT COUNT(*) FROM transactions")
        count = c.fetchone()[0]
        
        if count == 0:
            # Generate demo data
            companies = ["RELIANCE", "TCS", "INFY"]
            generate_demo_transactions(conn, companies)
        
        # Load transactions with proper type conversion
        df = pd.read_sql_query("""
            SELECT 
                datetime(timestamp) as timestamp,
                stock,
                action,
                CAST(quantity as INTEGER) as quantity,
                CAST(price as FLOAT) as price,
                CAST(quantity as INTEGER) * CAST(price as FLOAT) as total_amount
            FROM transactions
            ORDER BY timestamp DESC
        """, conn)
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['formatted_time'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        
        return df
    except Exception as e:
        st.error(f"Failed to load transactions: {str(e)}")
        return pd.DataFrame()

def format_currency(value):
    try:
        return f"₹{float(value):,.2f}"
    except:
        return value

def main():
    st.title("💸 Real-Time Transaction Portal")
    
    # Add demo mode notice
    st.info("🔄 Demo Mode: Showing simulated trading activity for demonstration purposes")
    
    # Load transactions
    df = load_transactions()
    
    if df.empty:
        st.warning("No transactions found")
        return

    # Summary metrics with descriptions
    st.subheader("📊 Trading Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_invested = df[df['action'] == 'BUY']['total_amount'].sum()
        st.metric("Total Invested", f"₹{total_invested:,.2f}")
        st.caption("Total capital deployed in buying stocks")
    
    with col2:
        total_sold = df[df['action'] == 'SELL']['total_amount'].sum()
        st.metric("Total Sold", f"₹{total_sold:,.2f}")
        st.caption("Total value of sold positions")
    
    with col3:
        net_position = total_sold - total_invested
        st.metric("Net Position", f"₹{net_position:,.2f}", 
                 delta=f"₹{net_position/total_invested*100:.1f}%" if total_invested else "0%")
        st.caption("Current profit/loss position")
    
    with col4:
        trade_count = len(df)
        st.metric("Total Trades", trade_count)
        st.caption("Number of transactions executed")

    # Real-time trading visualization
    st.subheader("📈 Trading Activity")
    fig = px.scatter(df,
                    x='timestamp',
                    y='total_amount',
                    color='action',
                    size='quantity',
                    hover_data=['stock', 'price', 'quantity'],
                    title="Real-Time Trading Activity")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Transaction History
    st.subheader("📊 Transaction History")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_stocks = st.multiselect(
            "Filter by Stock",
            options=df['stock'].unique(),
            default=df['stock'].unique()
        )
    with col2:
        selected_actions = st.multiselect(
            "Filter by Action",
            options=df['action'].unique(),
            default=df['action'].unique()
        )
    
    # Filter dataframe
    filtered_df = df[
        (df['stock'].isin(selected_stocks)) &
        (df['action'].isin(selected_actions))
    ]
    
    try:
        # Transaction timeline using formatted timestamps
        fig = px.scatter(filtered_df,
                        x='formatted_time',
                        y='total_amount',
                        color='action',
                        size='quantity',
                        hover_data=['stock', 'price', 'quantity'],
                        title="Transaction Timeline")
        fig.update_xaxes(title="Time")
        fig.update_yaxes(title="Amount (₹)")
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Failed to create transaction timeline: {str(e)}")
    
    # Detailed transaction table with proper formatting
    st.subheader("📝 Detailed Transactions")
    if not filtered_df.empty:
        # Convert to string before display
        display_df = filtered_df.copy()
        display_df['price'] = display_df['price'].apply(lambda x: f"₹{float(x):,.2f}")
        display_df['total_amount'] = display_df['total_amount'].apply(lambda x: f"₹{float(x):,.2f}")
        st.dataframe(display_df)
    else:
        st.info("No transactions to display")

    # Stock-wise summary with proper formatting
    st.subheader("📈 Stock-wise Summary")
    if not filtered_df.empty:
        summary = filtered_df.groupby('stock').agg({
            'total_amount': ['sum', 'mean'],
            'quantity': 'sum'
        }).round(2)
        summary.columns = ['Total Amount', 'Average Amount', 'Total Quantity']
        
        # Format currency columns
        summary['Total Amount'] = summary['Total Amount'].apply(format_currency)
        summary['Average Amount'] = summary['Average Amount'].apply(format_currency)
        
        st.dataframe(summary)
    else:
        st.info("No summary data available")

if __name__ == "__main__":
    main()
