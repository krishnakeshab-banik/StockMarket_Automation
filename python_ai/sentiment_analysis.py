import requests
from textblob import TextBlob
import json
import os

# Step 1: Your NewsAPI Key
api_key = "8a770f21ee7c48a996e192eba61a68d9"

# Step 2: Companies to track
companies = ["Reliance", "TCS", "HDFC Bank"]

# Step 3: Define absolute path to save JSON
data_folder = r"C:\Users\godre\Desktop\AI_Stock_Automation\data"
os.makedirs(data_folder, exist_ok=True)  # ensures folder exists

# Step 4: Collect news and analyze sentiment
sentiment_results = {}

for company in companies:
    url = f"https://newsapi.org/v2/everything?q={company}&language=en&sortBy=publishedAt&pageSize=5&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] != "ok":
        print(f"Error fetching news for {company}")
        continue

    headlines = [article["title"] for article in data["articles"]]
    total_score = 0
    for headline in headlines:
        total_score += TextBlob(headline).sentiment.polarity
    
    avg_score = total_score / max(len(headlines), 1)
    
    if avg_score > 0.1:
        action = "Buy"
    elif avg_score < -0.1:
        action = "Sell"
    else:
        action = "Hold"
    
    sentiment_results[company] = {
        "average_sentiment": round(avg_score, 2),
        "action": action,
        "headlines": headlines
    }

# Step 5: Save results to JSON
output_file = os.path.join(data_folder, "real_time_sentiment.json")
with open(output_file, "w") as f:
    json.dump(sentiment_results, f, indent=4)

print("✅ Real-time sentiment analysis complete:")
print(json.dumps(sentiment_results, indent=4))
