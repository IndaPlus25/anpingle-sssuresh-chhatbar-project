"""Visual assets for candlestick rendering - defines dimensions and rendering styles."""

# Candlestick rendering dimensions
CANDLE_WIDTH = 10
CANDLE_SPACING = 4
CANDLE_WICK_WIDTH = 2
CANDLE_BODY_BORDER_WIDTH = 1

# Color schemes for candles
CANDLE_COLORS = {
    "bullish": {
        "body": (0, 200, 100),       # Bright green body
        "border": (0, 100, 0),        # Dark green border
        "wick": (0, 100, 0),          # Dark green wick
        "text": (255, 255, 255),      # White text
    },
    "bearish": {
        "body": (200, 50, 50),        # Bright red body
        "border": (139, 0, 0),        # Dark red border
        "wick": (139, 0, 0),          # Dark red wick
        "text": (255, 255, 255),      # White text
    },
    "doji": {
        "body": (128, 128, 128),      # Gray body
        "border": (64, 64, 64),       # Dark gray border
        "wick": (64, 64, 64),         # Dark gray wick
        "text": (255, 255, 255),      # White text
    },
}

# Chart styling
CHART_STYLING = {
    "background": (240, 240, 240),   # Light gray background
    "border": (0, 0, 0),              # Black border
    "grid": (200, 200, 200),         # Light gray grid lines
    "axis_text": (50, 50, 50),       # Dark gray text
    "title": (0, 0, 0),              # Black title
    "subtitle": (100, 100, 100),     # Medium gray subtitle
}

# Text positions relative to chart
TEXT_OFFSETS = {
    "title": (0, -25),
    "subtitle": (0, -10),
    "price_label": (5, 5),
}

# Pattern progress visualization
PATTERN_PROGRESS = {
    "indicator_size": 4,              # Size of progress dots
    "indicator_spacing": 6,           # Spacing between progress indicators
    "max_indicators": 20,             # Max indicators to show
}

# Animation settings for pattern formation
ANIMATION_SETTINGS = {
    "flash_color": (255, 255, 0),     # Yellow flash for pattern start
    "flash_duration": 30,             # Frames to flash
    "pulse_speed": 0.05,              # Speed of pattern progress pulse
}


def get_candle_color(is_bullish, is_doji=False):
    """Get the color scheme dict for a candle based on type."""
    if is_doji:
        return CANDLE_COLORS["doji"]
    return CANDLE_COLORS["bullish"] if is_bullish else CANDLE_COLORS["bearish"]


def calculate_chart_dimensions(candles, max_candles=50):
    """Calculate optimal chart dimensions based on candle count."""
    if not candles:
        return None

    visible_candles = min(len(candles), max_candles)
    chart_width = visible_candles * (CANDLE_WIDTH + CANDLE_SPACING) + 20
    chart_height = 150

    # Get price range
    min_price = min(c.low for c in candles[-visible_candles:])
    max_price = max(c.high for c in candles[-visible_candles:])
    price_range = max(max_price - min_price, 1)

    return {
        "width": chart_width,
        "height": chart_height,
        "min_price": min_price,
        "max_price": max_price,
        "range": price_range,
    }
