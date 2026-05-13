import random
from game.stocks.patterns import PATTERNS

def generate_random_story(stocks):
    stock = random.choice(stocks)
    ticker = stock.name
    price = stock.price
    
    # Generate realistic-looking price movement stats
    change_pct  = round(random.uniform(1.5, 18.0), 2)
    volume_m    = round(random.uniform(1.2, 94.0), 1)
    target      = round(price * random.uniform(1.05, 1.40), 2)
    competitor  = random.choice([s.name for s in stocks if s.name != ticker])
    analyst     = random.choice(["Goldman Sachs", "Morgan Stanley", "JPMorgan", "Citi", "UBS", "Deutsche Bank"])
    exec_name   = random.choice(["CEO", "CFO", "COO", "Chairman"])

    impact = random.choice(["positive", "negative", "neutral"])

    templates = {
        "positive": [
            {
                "headline": f"{ticker} surges {change_pct}% on strong earnings",
                "summary":  f"{ticker} beat analyst expectations this quarter, sending shares up {change_pct}%.",
                "body":     f"{ticker} reported earnings well above consensus estimates, driven by record revenue and expanding margins. Trading volume hit {volume_m}M shares. {analyst} raised their price target to ${target}, citing strong forward guidance."
            },
            {
                "headline": f"Analysts upgrade {ticker}, set target of ${target}",
                "summary":  f"{analyst} raised its price target on {ticker} to ${target} after better-than-expected results.",
                "body":     f"In a note to clients, {analyst} upgraded {ticker} from Neutral to Buy, setting a 12-month price target of ${target}. The firm cited improving margins and a favorable macro environment as key drivers of the upgrade."
            },
            {
                "headline": f"{ticker} announces ${ round(random.uniform(0.5, 5.0), 1)}B share buyback",
                "summary":  f"{ticker} management announced a major buyback program, boosting investor confidence.",
                "body":     f"The {exec_name} of {ticker} announced a share repurchase program worth billions, signaling confidence in the company's long-term outlook. Shares jumped {change_pct}% on the news, with volume reaching {volume_m}M — well above the 30-day average."
            },
            {
                "headline": f"{ticker} hits 52-week high amid sector rally",
                "summary":  f"{ticker} reached a new 52-week high today as the broader sector gained momentum.",
                "body":     f"Buoyed by positive sentiment across the sector, {ticker} climbed {change_pct}% to set a new 52-week high. Analysts at {analyst} noted the stock still trades at a discount to peers, leaving room for further upside toward their ${target} target."
            },
        ],
        "negative": [
            {
                "headline": f"{ticker} drops {change_pct}% after missing revenue targets",
                "summary":  f"{ticker} fell sharply after quarterly revenue came in below Wall Street expectations.",
                "body":     f"{ticker} reported revenue that missed consensus by a wide margin, triggering a sell-off of {change_pct}%. The {exec_name} acknowledged headwinds but maintained full-year guidance. {analyst} cut their price target, and volume spiked to {volume_m}M shares on the day."
            },
            {
                "headline": f"Scandal rocks {ticker}, shares slide {change_pct}%",
                "summary":  f"Reports of internal misconduct at {ticker} sent shares tumbling {change_pct}% in heavy trading.",
                "body":     f"Leaked documents suggested irregularities in {ticker}'s accounting practices, prompting a swift market reaction. Shares fell {change_pct}% on volume of {volume_m}M. The {exec_name} issued a brief statement denying wrongdoing, but investor confidence remained shaken."
            },
            {
                "headline": f"{analyst} downgrades {ticker} to Sell",
                "summary":  f"{analyst} cut its rating on {ticker} to Sell, citing deteriorating fundamentals.",
                "body":     f"In a bearish note, {analyst} downgraded {ticker} from Hold to Sell, slashing their price target significantly. The firm pointed to rising costs, slowing growth, and increased competition from {competitor} as reasons for the more cautious stance."
            },
            {
                "headline": f"{ticker} loses ground as {competitor} gains market share",
                "summary":  f"Investors rotated out of {ticker} and into rival {competitor} following a competitive product launch.",
                "body":     f"{competitor}'s new product announcement appears to be weighing on {ticker}, which fell {change_pct}% in today's session on volume of {volume_m}M shares. Several analysts flagged the competitive threat as a risk to {ticker}'s near-term revenue outlook."
            },
        ],
        "neutral": [
            {
                "headline": f"{ticker} {exec_name} speaks at investor day",
                "summary":  f"{ticker}'s {exec_name} outlined the company's five-year strategic roadmap at today's investor day.",
                "body":     f"At its annual investor day, {ticker}'s {exec_name} presented a long-term growth strategy focused on geographic expansion and R&D investment. Shares moved less than 1% on the day, with {volume_m}M shares changing hands. {analyst} maintained their Hold rating and ${target} price target."
            },
            {
                "headline": f"Market watches {ticker} ahead of earnings report",
                "summary":  f"Investors are cautiously positioning around {ticker} with earnings due later this week.",
                "body":     f"With {ticker}'s quarterly results expected imminently, options activity has picked up significantly. Implied volatility suggests the market is pricing in a move of roughly {change_pct}% in either direction. {analyst} reiterated a Neutral rating with a ${target} target ahead of the print."
            },
            {
                "headline": f"{ticker} and {competitor} explore potential partnership",
                "summary":  f"Reports suggest {ticker} and {competitor} are in early talks over a strategic collaboration.",
                "body":     f"Sources familiar with the matter indicated that {ticker} and {competitor} have held preliminary discussions about a technology-sharing agreement. Neither company has confirmed the talks. Analysts say a deal could be modestly positive for both, though execution risk remains high."
            },
            {
                "headline": f"{ticker} trading volume spikes to {volume_m}M with no clear catalyst",
                "summary":  f"Unusual volume in {ticker} has traders speculating, though the stock moved less than 1%.",
                "body":     f"{ticker} saw {volume_m}M shares trade hands today — roughly three times the daily average — without any obvious news catalyst. Some traders attributed the activity to algorithmic rebalancing, while others speculated about undisclosed institutional activity. The stock closed nearly flat."
            },
        ],
    }

    story = random.choice(templates[impact])
    return {
        "ticker":    ticker,
        "impact":    impact,
        "headline":  story["headline"],
        "summary":   story["summary"],
        "body":      story["body"],
        "timestamp": "Just Now",
    }

class News:
    def __init__(self, news_items=None):
        self.news_items = news_items or []
        self.scroll_offset = 0

    def add_item(self, item):
        self.news_items.insert(0, item)  # newest first

    def apply_to_stocks(self, stocks):
        """
        Injects a pattern into the relevant stock based on news impact,
        working with the GBM engine rather than nudging price directly.
        """
        if not self.news_items:
            return

        item = self.news_items[0]
        ticker = item.get("ticker")
        impact = item.get("impact", "neutral")

        IMPACT_PATTERNS = {
            "positive": [
                "bullish_engulfing", "morning_star", "three_white_soldiers",
                "bullish_kicker", "bullish_abandoned_baby", "rising_three_methods",
                "bullish_mat_hold", "rounding_bottom",
            ],
            "negative": [
                "bearish_engulfing", "evening_star", "three_black_crows",
                "bearish_kicker", "bearish_abandoned_baby", "falling_three_methods",
                "rounding_top", "triple_top",
            ],
            "neutral": [
                "bearish_spinning_top", "bearish_harami", "bullish_harami",
                "dragonfly_doji", "gravestone_doji",
            ],
        }

        pattern_name = random.choice(IMPACT_PATTERNS.get(impact, IMPACT_PATTERNS["neutral"]))

        for stock in stocks:
            if stock.name == ticker:
                stock.inject_named_pattern(pattern_name)
                break

    def scroll(self, amount):
        self.scroll_offset = max(0, self.scroll_offset + amount)