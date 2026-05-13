"""Stock visual assets — candlestick rendering dimensions, colors, pattern labels,
chart styling, and helper utilities.

Consolidates the former ``candles.py`` and ``patterns.py`` into a single module
so that all stock-related visual constants live in one place.
"""

# ---------------------------------------------------------------------------
#  Candlestick rendering dimensions
# ---------------------------------------------------------------------------
CANDLE_WIDTH = 10
CANDLE_SPACING = 4
CANDLE_WICK_WIDTH = 2
CANDLE_BODY_BORDER_WIDTH = 1

# ---------------------------------------------------------------------------
#  Color schemes for individual candles
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
#  Chart styling
# ---------------------------------------------------------------------------
CHART_STYLING = {
    "background": (240, 240, 240),   # Light gray background
    "border": (0, 0, 0),              # Black border
    "grid": (200, 200, 200),         # Light gray grid lines
    "axis_text": (50, 50, 50),       # Dark gray text
    "title": (0, 0, 0),              # Black title
    "subtitle": (100, 100, 100),     # Medium gray subtitle
}

# ---------------------------------------------------------------------------
#  Text positions relative to chart
# ---------------------------------------------------------------------------
TEXT_OFFSETS = {
    "title": (0, -25),
    "subtitle": (0, -10),
    "price_label": (5, 5),
}

# ---------------------------------------------------------------------------
#  Pattern progress visualization
# ---------------------------------------------------------------------------
PATTERN_PROGRESS = {
    "indicator_size": 4,              # Size of progress dots
    "indicator_spacing": 6,           # Spacing between progress indicators
    "max_indicators": 20,             # Max indicators to show
}

# Progress bar background color (used by pygame.py drawing routines)
PATTERN_PROGRESS_BG = (60, 60, 60)

# ---------------------------------------------------------------------------
#  Animation settings for pattern formation
# ---------------------------------------------------------------------------
ANIMATION_SETTINGS = {
    "flash_color": (255, 255, 0),     # Yellow flash for pattern start
    "flash_duration": 30,             # Frames to flash
    "pulse_speed": 0.05,              # Speed of pattern progress pulse
}

# ---------------------------------------------------------------------------
#  Pattern category colors
# ---------------------------------------------------------------------------
PATTERN_COLORS = {
    "bullish_reversal": (0, 200, 100),      # Bright green
    "bearish_reversal": (200, 50, 50),      # Bright red
    "bullish_continuation": (50, 150, 80),   # Muted green
    "bearish_continuation": (150, 50, 50),   # Muted red
    "doji": (128, 128, 128),                 # Gray
}

# ---------------------------------------------------------------------------
#  Pattern type labels
#  Each entry: pattern_key -> (DISPLAY_NAME, Category, color_category_key)
# ---------------------------------------------------------------------------
PATTERN_LABELS = {
    # Bullish Reversal
    "hammer": ("HAMMER", "Bullish Reversal", "bullish_reversal"),
    "inverted_hammer": ("INVERTED HAMMER", "Bullish Reversal", "bullish_reversal"),
    "bullish_engulfing": ("BULLISH ENGULFING", "Bullish Reversal", "bullish_reversal"),
    "piercing_line": ("PIERCING LINE", "Bullish Reversal", "bullish_reversal"),
    "morning_star": ("MORNING STAR", "Bullish Reversal", "bullish_reversal"),
    "three_white_soldiers": ("THREE WHITE SOLDIERS", "Bullish Reversal", "bullish_reversal"),
    "three_inside_up": ("THREE INSIDE UP", "Bullish Reversal", "bullish_reversal"),
    "bullish_harami": ("BULLISH HARAMI", "Bullish Reversal", "bullish_reversal"),
    "tweezer_bottom": ("TWEEZER BOTTOM", "Bullish Reversal", "bullish_reversal"),
    "bullish_counterattack": ("BULLISH COUNTERATTACK", "Bullish Reversal", "bullish_reversal"),
    "bullish_kicker": ("BULLISH KICKER", "Bullish Reversal", "bullish_reversal"),
    "bullish_abandoned_baby": ("BULLISH ABANDONED BABY", "Bullish Reversal", "bullish_reversal"),
    "morning_star_doji": ("MORNING STAR DOJI", "Bullish Reversal", "bullish_reversal"),
    "dragonfly_doji": ("DRAGONFLY DOJI", "Bullish Reversal", "doji"),
    "bullish_tri_star": ("BULLISH TRI-STAR", "Bullish Reversal", "bullish_reversal"),
    "bullish_hikkake": ("BULLISH HIKKAKE", "Bullish Reversal", "bullish_reversal"),
    "concealing_baby_swallow": ("CONCEALING BABY SWALLOW", "Bullish Reversal", "bullish_reversal"),
    "unique_three_rivers": ("UNIQUE THREE RIVERS", "Bullish Reversal", "bullish_reversal"),
    "rounding_bottom": ("ROUNDING BOTTOM", "Bullish Reversal", "bullish_reversal"),
    "bullish_belt_hold": ("BULLISH BELT HOLD", "Bullish Reversal", "bullish_reversal"),
    "bullish_mat_hold": ("BULLISH MAT HOLD", "Bullish Reversal", "bullish_reversal"),
    "rising_three_methods": ("RISING THREE METHODS", "Bullish Continuation", "bullish_continuation"),
    "homing_pigeon": ("HOMING PIGEON", "Bullish Reversal", "bullish_reversal"),
    "stick_sandwich": ("STICK SANDWICH", "Bullish Reversal", "bullish_reversal"),
    # Bearish Reversal
    "hanging_man": ("HANGING MAN", "Bearish Reversal", "bearish_reversal"),
    "dark_cloud_cover": ("DARK CLOUD COVER", "Bearish Reversal", "bearish_reversal"),
    "bearish_engulfing": ("BEARISH ENGULFING", "Bearish Reversal", "bearish_reversal"),
    "evening_star": ("EVENING STAR", "Bearish Reversal", "bearish_reversal"),
    "three_black_crows": ("THREE BLACK CROWS", "Bearish Reversal", "bearish_reversal"),
    "three_inside_down": ("THREE INSIDE DOWN", "Bearish Reversal", "bearish_reversal"),
    "bearish_harami": ("BEARISH HARAMI", "Bearish Reversal", "bearish_reversal"),
    "shooting_star": ("SHOOTING STAR", "Bearish Reversal", "bearish_reversal"),
    "tweezer_top": ("TWEEZER TOP", "Bearish Reversal", "bearish_reversal"),
    "bearish_counterattack": ("BEARISH COUNTERATTACK", "Bearish Reversal", "bearish_reversal"),
    "bearish_spinning_top": ("BEARISH SPINNING TOP", "Bearish Reversal", "doji"),
    "bearish_kicker": ("BEARISH KICKER", "Bearish Reversal", "bearish_reversal"),
    "evening_star_doji": ("EVENING STAR DOJI", "Bearish Reversal", "bearish_reversal"),
    "bearish_abandoned_baby": ("BEARISH ABANDONED BABY", "Bearish Reversal", "bearish_reversal"),
    "gravestone_doji": ("GRAVESTONE DOJI", "Bearish Reversal", "doji"),
    "bearish_tri_star": ("BEARISH TRI-STAR", "Bearish Reversal", "bearish_reversal"),
    "deliberation": ("DELIBERATION", "Bearish Reversal", "bearish_reversal"),
    "upside_gap_two_crows": ("UPSIDE GAP TWO CROWS", "Bearish Reversal", "bearish_reversal"),
    "advance_block": ("ADVANCE BLOCK", "Bearish Reversal", "bearish_reversal"),
    # Bearish Continuation
    "rounding_top": ("ROUNDING TOP", "Bearish Continuation", "bearish_continuation"),
    "triple_top": ("TRIPLE TOP", "Bearish Continuation", "bearish_continuation"),
    "falling_three_methods": ("FALLING THREE METHODS", "Bearish Continuation", "bearish_continuation"),
    "on_neck": ("ON NECK PATTERN", "Bearish Continuation", "bearish_continuation"),
    "in_neck": ("IN NECK PATTERN", "Bearish Continuation", "bearish_continuation"),
}


# ---------------------------------------------------------------------------
#  Helper functions
# ---------------------------------------------------------------------------

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


def get_pattern_color(pattern_name):
    """Get the color tuple for a pattern name."""
    if pattern_name is None:
        return None
    _, _, category = PATTERN_LABELS.get(pattern_name, (None, None, None))
    return PATTERN_COLORS.get(category)


def get_pattern_info(pattern_name):
    """Get pattern name, category, and color for display."""
    if pattern_name is None:
        return None
    return PATTERN_LABELS.get(pattern_name)
