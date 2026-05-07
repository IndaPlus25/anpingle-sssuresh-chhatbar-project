"""Visual assets for candlestick patterns - defines colors and visual styles."""

# Pattern category colors
PATTERN_COLORS = {
    "bullish_reversal": (0, 200, 100),      # Bright green
    "bearish_reversal": (200, 50, 50),      # Bright red
    "bullish_continuation": (50, 150, 80),   # Muted green
    "bearish_continuation": (150, 50, 50),   # Muted red
    "doji": (128, 128, 128),                 # Gray
}

# Pattern type labels
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
