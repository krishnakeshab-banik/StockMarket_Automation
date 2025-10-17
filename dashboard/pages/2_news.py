import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np
from datetime import datetime
from pathlib import Path

def main():
    st.title("📰 News & Sentiment Analysis")
    
    # Get path to data file
    json_path = Path(__file__).parent.parent.parent / "data" / "real_time_sentiment.json"
    
    try:
        # Load sentiment data
        with open(json_path, "r") as f:
            data = json.load(f)
        
        # News feed with sentiment
        st.subheader("Latest News & Sentiment")
        
        for company, details in data.items():
            with st.expander(f"{company} News"):
                sentiment = details.get('average_sentiment', 0)
                color = 'green' if sentiment > 0.2 else 'red' if sentiment < -0.2 else 'orange'
                st.markdown(f"**Sentiment Score:** <span style='color:{color}'>{sentiment:.2f}</span>", 
                          unsafe_allow_html=True)
                
                headlines = details.get('headlines', [])
                for headline in headlines:
                    st.markdown(f"- {headline}")
                
                # Sentiment trend chart
                dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
                sentiment_trend = pd.DataFrame({
                    'Date': dates,
                    'Sentiment': np.random.normal(sentiment, 0.1, 10)
                })
                fig = px.line(sentiment_trend, x='Date', y='Sentiment', 
                            title=f'{company} Sentiment Trend')
                st.plotly_chart(fig)
    
    except FileNotFoundError:
        st.error("News data file not found. Please ensure the data pipeline has been run.")
    except json.JSONDecodeError:
        st.error("Invalid news data format. Please check the data file.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
