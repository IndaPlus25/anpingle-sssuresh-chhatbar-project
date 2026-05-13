import random

def generate_random_story(stocks):
        ticker = random.choice([s.name for s in stocks])
        impact = random.choice(["positive", "negative", "neutral"])
        
        # Simple template logic
        headlines = {
            "positive": [f"{ticker} hits all-time high!", f"New breakthrough for {ticker}"],
            "negative": [f"Scandal at {ticker} HQ", f"Investors flee {ticker} after report"],
            "neutral":  [f"{ticker} CEO speaks at conference", f"Market analyzes {ticker} outlook"]
        }
        
        return {
            "ticker": ticker,
            "impact": impact,
            "headline": random.choice(headlines[impact]),
            "summary": f"Dramatic shifts observed in {ticker} trading volume today.",
            "body": "Detailed market analysis suggests that current trends are likely to continue for the foreseeable future.",
            "timestamp": "Just Now"
        }

class News:
    def __init__(self, news_items=None):
        self.news_items = news_items or []
        self.scroll_offset = 0

    def add_item(self, item):
        self.news_items.insert(0, item)  # newest first

    def apply_to_stocks(self, stocks):
        """
        Applies the most recent news item's impact to the relevant stock.
        Looks for a stock matching the item's ticker and nudges its price.
        """
        if not self.news_items:
            return

        item = self.news_items[0]
        ticker = item.get("ticker")
        impact = item.get("impact", "neutral")

        IMPACT_RANGES = {
            "positive": (2.0, 15.0),
            "negative": (-15.0, -2.0),
            "neutral":  (-2.0, 2.0),
        }

        low, high = IMPACT_RANGES.get(impact, (-2.0, 2.0))
        change = random.uniform(low, high)

        for stock in stocks:
            if stock.name == ticker:
                stock.price += change
                stock.price = max(0.01, round(stock.price, 2))
                break

    def scroll(self, amount):
        self.scroll_offset += amount
        # Optional: Prevent scrolling above 0
        if self.scroll_offset < 0:
            self.scroll_offset = 0