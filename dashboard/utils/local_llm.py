class LocalStockAdvisor:
    def __init__(self):
        self.knowledge_base = {
            "market_conditions": {
                "bullish": "The market shows positive trends. Consider buying opportunities.",
                "bearish": "Market indicators suggest caution. Consider protecting positions.",
                "neutral": "Market conditions are stable. Monitor for changes."
            },
            "stock_actions": {
                "buy": "Technical analysis suggests a buying opportunity for {stock}.",
                "sell": "Consider taking profits or cutting losses for {stock}.",
                "hold": "Current position in {stock} appears optimal."
            }
        }

    def get_response(self, prompt, context):
        prompt = prompt.lower()
        
        # Extract context information
        try:
            portfolio = eval(context.split("Portfolio: ")[1].split("\n")[0])
            sentiments = eval(context.split("Market Sentiment: ")[1])
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        except:
            portfolio = {}
            avg_sentiment = 0

        # Generate response based on query type
        if "market" in prompt or "overall" in prompt:
            if avg_sentiment > 0.2:
                return self.knowledge_base["market_conditions"]["bullish"]
            elif avg_sentiment < -0.2:
                return self.knowledge_base["market_conditions"]["bearish"]
            return self.knowledge_base["market_conditions"]["neutral"]

        # Stock specific queries
        for stock in portfolio.keys():
            if stock.lower() in prompt:
                if "buy" in prompt:
                    return self.knowledge_base["stock_actions"]["buy"].format(stock=stock)
                elif "sell" in prompt:
                    return self.knowledge_base["stock_actions"]["sell"].format(stock=stock)
                return self.knowledge_base["stock_actions"]["hold"].format(stock=stock)

        return "I can help you analyze market conditions and specific stocks. Try asking about market trends or specific companies."
