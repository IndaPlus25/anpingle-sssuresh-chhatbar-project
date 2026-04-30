# patterns.py
# Each pattern is a list of (ticks, drift) tuples.
# Positive drift = bullish pressure, negative = bearish.
# Ticks represent candlestick periods.
# These are injected sequentially into the GBM engine in stock.py.

# ---------------------------------------------------------------------------
# BULLISH REVERSAL PATTERNS
# Context: Should be injected after a downtrend (negative mu phase).
# ---------------------------------------------------------------------------

# 1. Hammer — single candle, sharp rejection of lows, small body
HAMMER = [
    (3, -0.005),   # brief continued drop (the lower wick)
    (2,  0.009),   # sharp snap back close (small bullish body)
]

# 2. Inverted Hammer — small body, long upper wick after downtrend
INVERTED_HAMMER = [
    (2,  0.007),   # buying attempt pushes price up (upper wick)
    (2, -0.003),   # partial rejection, closes near open
    (3,  0.006),   # confirmation bullish candle
]

# 3. Bullish Engulfing — large bullish candle engulfs prior bearish
BULLISH_ENGULFING = [
    (3, -0.006),   # prior bearish candle
    (4,  0.012),   # large bullish engulfing candle
]

# 4. Piercing Line — bullish close above midpoint of prior bearish
PIERCING_LINE = [
    (3, -0.007),   # bearish candle
    (1, -0.003),   # gap down open
    (3,  0.009),   # bullish recovery past midpoint
]

# 5. Morning Star — bearish, doji, strong bullish
MORNING_STAR = [
    (4, -0.007),   # large bearish candle
    (3,  0.000),   # small indecisive candle (doji-like)
    (4,  0.010),   # large bullish confirmation
]

# 6. Three White Soldiers — three consecutive strong bullish candles
THREE_WHITE_SOLDIERS = [
    (5,  0.007),
    (5,  0.007),
    (5,  0.008),
]

# 7. Three Inside Up — harami then bullish confirmation
THREE_INSIDE_UP = [
    (4, -0.007),   # large bearish
    (3,  0.003),   # small bullish inside (harami)
    (4,  0.008),   # bullish confirmation above first candle
]

# 8. Bullish Harami — small bullish inside prior large bearish
BULLISH_HARAMI = [
    (4, -0.008),   # large bearish
    (3,  0.003),   # small bullish inside
]

# 9. Tweezer Bottom — two candles hitting same low, then bounce
TWEEZER_BOTTOM = [
    (3, -0.006),   # bearish to a low
    (1,  0.000),   # retests same low (flat)
    (3,  0.007),   # bullish bounce
]

# 10. Bullish Counterattack — drop then close near prior close
BULLISH_COUNTERATTACK = [
    (3, -0.008),   # bearish drop
    (3,  0.007),   # sharp recovery to prior close level
    (3,  0.004),   # confirmation
]

# 11. Bullish Kicker — gap up after bearish, strong sentiment shift
BULLISH_KICKER = [
    (3, -0.006),   # bearish candle
    (1,  0.015),   # gap up (large jump)
    (3,  0.007),   # continued bullish
]

# 12. Bullish Abandoned Baby — doji gap, then gap up bullish
BULLISH_ABANDONED_BABY = [
    (3, -0.007),   # bearish phase
    (1, -0.008),   # gap down to doji (low point)
    (1,  0.000),   # doji candle (indecision)
    (1,  0.010),   # gap up
    (3,  0.007),   # bullish continuation
]

# 13. Morning Star Doji — like morning star but middle is pure doji
MORNING_STAR_DOJI = [
    (4, -0.008),   # large bearish
    (2,  0.000),   # pure doji (open ≈ close)
    (4,  0.010),   # bullish reversal
]

# 14. Dragonfly Doji — long lower shadow, close near high
DRAGONFLY_DOJI = [
    (2, -0.008),   # deep lower wick
    (3,  0.009),   # recovery to near session high
    (3,  0.005),   # confirmation
]

# 15. Bullish Tri-Star — three dojis then reversal
BULLISH_TRI_STAR = [
    (2,  0.000),   # doji 1
    (2,  0.000),   # doji 2
    (2,  0.000),   # doji 3
    (4,  0.008),   # bullish reversal
]

# 16. Bullish Hikkake — false breakdown then reversal up
BULLISH_HIKKAKE = [
    (3, -0.004),   # inside bar setup
    (2, -0.007),   # false bearish breakout
    (4,  0.010),   # sharp reversal upward
]

# 17. Concealing Baby Swallow — two strong bearish, then engulfing bullish
CONCEALING_BABY_SWALLOW = [
    (4, -0.008),   # strong bearish 1
    (4, -0.007),   # strong bearish 2
    (5,  0.012),   # large engulfing bullish
]

# 18. Unique Three Rivers — exhaustion and small rebound
UNIQUE_THREE_RIVERS = [
    (3, -0.008),   # large bearish
    (3, -0.004),   # inside bearish with low wick
    (3,  0.005),   # small bullish rebound
]

# 19. Rounding Bottom — slow curved base then uptrend
ROUNDING_BOTTOM = [
    (10, -0.003),  # gradual decline
    (10,  0.000),  # flat base / accumulation
    (10,  0.003),  # gradual rise
    (5,   0.007),  # breakout
]

# 20. Bullish Belt Hold — opens at low, closes near high
BULLISH_BELT_HOLD = [
    (1,  0.000),   # opens at low (no lower wick)
    (5,  0.009),   # strong bullish run to close
]

# 21. Mat Hold (Bullish) — uptrend, pause, continuation
BULLISH_MAT_HOLD = [
    (5,  0.008),   # initial bullish candle
    (3, -0.003),   # small pullback (consolidation)
    (3,  0.001),   # sideways
    (5,  0.009),   # continuation upward
]

# 22. Rising Three Methods — bullish, small bearish pullback, bullish continuation
RISING_THREE_METHODS = [
    (5,  0.008),   # strong bullish
    (2, -0.002),   # small bearish 1
    (2, -0.002),   # small bearish 2
    (2, -0.002),   # small bearish 3
    (5,  0.009),   # strong bullish continuation
]

# 23. Homing Pigeon — second bearish inside first bearish, then reversal
HOMING_PIGEON = [
    (4, -0.007),   # large bearish
    (3, -0.003),   # smaller bearish inside
    (4,  0.008),   # bullish confirmation
]

# 24. Stick Sandwich — bear-bull-bear with same closes, then bounce
STICK_SANDWICH = [
    (3, -0.006),   # bearish
    (3,  0.007),   # bullish recovery
    (3, -0.005),   # bearish close at same level
    (4,  0.008),   # bullish reversal
]

# ---------------------------------------------------------------------------
# BEARISH REVERSAL PATTERNS
# Context: Should be injected after an uptrend (positive mu phase).
# ---------------------------------------------------------------------------

# 25. Hanging Man — small body, long lower wick at market top
HANGING_MAN = [
    (3,  0.005),   # up into the candle
    (2, -0.007),   # lower wick (selling pressure)
    (2,  0.004),   # close near open (small body)
    (3, -0.007),   # confirmation bearish
]

# 26. Dark Cloud Cover — bullish then bearish closes below midpoint
DARK_CLOUD_COVER = [
    (3,  0.007),   # bullish candle
    (1,  0.005),   # gap up open
    (4, -0.010),   # bearish close below midpoint
]

# 27. Bearish Engulfing — large bearish engulfs prior bullish
BEARISH_ENGULFING = [
    (3,  0.006),   # prior bullish candle
    (4, -0.012),   # large bearish engulfing
]

# 28. Evening Star — bullish, doji/small, strong bearish
EVENING_STAR = [
    (4,  0.007),   # large bullish
    (3,  0.000),   # small indecisive candle
    (4, -0.010),   # large bearish reversal
]

# 29. Three Black Crows — three consecutive strong bearish candles
THREE_BLACK_CROWS = [
    (5, -0.007),
    (5, -0.007),
    (5, -0.008),
]

# 30. Three Inside Down — bearish harami then confirmation
THREE_INSIDE_DOWN = [
    (4,  0.007),   # large bullish
    (3, -0.003),   # small bearish inside (harami)
    (4, -0.008),   # bearish confirmation below first candle
]

# 31. Bearish Harami — small bearish inside prior large bullish
BEARISH_HARAMI = [
    (4,  0.008),   # large bullish
    (3, -0.003),   # small bearish inside
]

# 32. Shooting Star — small body, long upper wick
SHOOTING_STAR = [
    (2,  0.009),   # upper wick (buying attempt)
    (2, -0.007),   # rejection, closes near low
    (3, -0.007),   # confirmation bearish
]

# 33. Tweezer Top — two candles hitting same high, then drop
TWEEZER_TOP = [
    (3,  0.006),   # bullish to a high
    (1,  0.000),   # retests same high (flat)
    (3, -0.007),   # bearish drop
]

# 34. Bearish Counterattack — rally then close near prior close
BEARISH_COUNTERATTACK = [
    (3,  0.008),   # bullish rally
    (3, -0.007),   # sharp drop to prior close
    (3, -0.004),   # confirmation
]

# 35. Bearish Spinning Top — small body, long wicks, indecision
BEARISH_SPINNING_TOP = [
    (2,  0.006),   # upper wick
    (2, -0.005),   # lower wick
    (1,  0.001),   # tiny body
    (4, -0.007),   # bearish follow-through
]

# 36. Bearish Kicker — gap down after bullish, sharp shift
BEARISH_KICKER = [
    (3,  0.006),   # bullish candle
    (1, -0.015),   # gap down
    (3, -0.007),   # continued bearish
]

# 37. Evening Star Doji — bullish, pure doji, bearish
EVENING_STAR_DOJI = [
    (4,  0.008),   # large bullish
    (2,  0.000),   # pure doji
    (4, -0.010),   # large bearish
]

# 38. Bearish Abandoned Baby — doji gap above, then gap down bearish
BEARISH_ABANDONED_BABY = [
    (3,  0.007),   # bullish phase
    (1,  0.008),   # gap up to doji
    (1,  0.000),   # doji
    (1, -0.010),   # gap down
    (3, -0.007),   # bearish continuation
]

# 39. Gravestone Doji — long upper wick, close near low
GRAVESTONE_DOJI = [
    (2,  0.008),   # upper wick (buying attempt)
    (3, -0.009),   # rejection back to open/low
    (3, -0.006),   # confirmation
]

# 40. Bearish Tri-Star — three dojis at top then reversal
BEARISH_TRI_STAR = [
    (2,  0.000),   # doji 1
    (2,  0.000),   # doji 2
    (2,  0.000),   # doji 3
    (4, -0.008),   # bearish reversal
]

# 41. Deliberation — three bullish candles with weakening third
DELIBERATION = [
    (4,  0.008),   # strong bullish 1
    (4,  0.007),   # strong bullish 2
    (4,  0.003),   # weakening bullish 3
    (4, -0.007),   # bearish reversal
]

# 42. Upside Gap Two Crows — gap up bullish, two bearish close gap
UPSIDE_GAP_TWO_CROWS = [
    (3,  0.009),   # bullish with gap up
    (3, -0.005),   # first bearish crow
    (4, -0.006),   # second bearish crow closes gap
]

# 43. Advance Block — three bullish with shrinking bodies
ADVANCE_BLOCK = [
    (4,  0.007),   # strong bullish
    (4,  0.005),   # weaker bullish
    (4,  0.003),   # weakest bullish
    (4, -0.008),   # bearish reversal
]

# ---------------------------------------------------------------------------
# BEARISH CONTINUATION PATTERNS
# Context: Inject during an ongoing downtrend.
# ---------------------------------------------------------------------------

# 44. Rounding Top — gradual peak then bearish continuation
ROUNDING_TOP = [
    (10,  0.003),  # gradual rise
    (10,  0.000),  # flat distribution top
    (10, -0.003),  # gradual decline
    (5,  -0.007),  # breakdown
]

# 45. Triple Top — three peaks at resistance then breakdown
TRIPLE_TOP = [
    (8,   0.007),  # rally to first top
    (5,  -0.005),  # pullback
    (8,   0.006),  # rally to second top (same level)
    (5,  -0.005),  # pullback
    (8,   0.005),  # rally to third top
    (6,  -0.010),  # breakdown below neckline
]

# 46. Falling Three Methods — bearish, small bullish pause, bearish continuation
FALLING_THREE_METHODS = [
    (5, -0.008),   # strong bearish
    (2,  0.002),   # small bullish 1
    (2,  0.002),   # small bullish 2
    (2,  0.002),   # small bullish 3
    (5, -0.009),   # strong bearish continuation
]

# 47. On Neck Pattern — bearish, small bullish close near prior low
ON_NECK = [
    (4, -0.008),   # bearish candle
    (3,  0.003),   # small bullish close at prior low
    (4, -0.007),   # bearish continuation
]

# 48. In Neck Pattern — bearish, slight recovery, continuation down
IN_NECK = [
    (4, -0.008),   # bearish candle
    (3,  0.002),   # tiny bullish recovery (just below prior close)
    (4, -0.007),   # bearish continuation
]

# ---------------------------------------------------------------------------
# REGISTRY — maps string names to pattern segment lists
# ---------------------------------------------------------------------------

PATTERNS = {
    # Bullish Reversal
    "hammer":                   HAMMER,
    "inverted_hammer":          INVERTED_HAMMER,
    "bullish_engulfing":        BULLISH_ENGULFING,
    "piercing_line":            PIERCING_LINE,
    "morning_star":             MORNING_STAR,
    "three_white_soldiers":     THREE_WHITE_SOLDIERS,
    "three_inside_up":          THREE_INSIDE_UP,
    "bullish_harami":           BULLISH_HARAMI,
    "tweezer_bottom":           TWEEZER_BOTTOM,
    "bullish_counterattack":    BULLISH_COUNTERATTACK,
    "bullish_kicker":           BULLISH_KICKER,
    "bullish_abandoned_baby":   BULLISH_ABANDONED_BABY,
    "morning_star_doji":        MORNING_STAR_DOJI,
    "dragonfly_doji":           DRAGONFLY_DOJI,
    "bullish_tri_star":         BULLISH_TRI_STAR,
    "bullish_hikkake":          BULLISH_HIKKAKE,
    "concealing_baby_swallow":  CONCEALING_BABY_SWALLOW,
    "unique_three_rivers":      UNIQUE_THREE_RIVERS,
    "rounding_bottom":          ROUNDING_BOTTOM,
    "bullish_belt_hold":        BULLISH_BELT_HOLD,
    "bullish_mat_hold":         BULLISH_MAT_HOLD,
    "rising_three_methods":     RISING_THREE_METHODS,
    "homing_pigeon":            HOMING_PIGEON,
    "stick_sandwich":           STICK_SANDWICH,
    # Bearish Reversal
    "hanging_man":              HANGING_MAN,
    "dark_cloud_cover":         DARK_CLOUD_COVER,
    "bearish_engulfing":        BEARISH_ENGULFING,
    "evening_star":             EVENING_STAR,
    "three_black_crows":        THREE_BLACK_CROWS,
    "three_inside_down":        THREE_INSIDE_DOWN,
    "bearish_harami":           BEARISH_HARAMI,
    "shooting_star":            SHOOTING_STAR,
    "tweezer_top":              TWEEZER_TOP,
    "bearish_counterattack":    BEARISH_COUNTERATTACK,
    "bearish_spinning_top":     BEARISH_SPINNING_TOP,
    "bearish_kicker":           BEARISH_KICKER,
    "evening_star_doji":        EVENING_STAR_DOJI,
    "bearish_abandoned_baby":   BEARISH_ABANDONED_BABY,
    "gravestone_doji":          GRAVESTONE_DOJI,
    "bearish_tri_star":         BEARISH_TRI_STAR,
    "deliberation":             DELIBERATION,
    "upside_gap_two_crows":     UPSIDE_GAP_TWO_CROWS,
    "advance_block":            ADVANCE_BLOCK,
    # Bearish Continuation
    "rounding_top":             ROUNDING_TOP,
    "triple_top":               TRIPLE_TOP,
    "falling_three_methods":    FALLING_THREE_METHODS,
    "on_neck":                  ON_NECK,
    "in_neck":                  IN_NECK,
}

# Metadata for each pattern (useful for game UI / quiz logic)
PATTERN_META = {
    "hammer":                   {"type": "bullish_reversal",      "reliability": "high"},
    "inverted_hammer":          {"type": "bullish_reversal",      "reliability": "medium"},
    "bullish_engulfing":        {"type": "bullish_reversal",      "reliability": "high"},
    "piercing_line":            {"type": "bullish_reversal",      "reliability": "medium"},
    "morning_star":             {"type": "bullish_reversal",      "reliability": "high"},
    "three_white_soldiers":     {"type": "bullish_continuation",  "reliability": "high"},
    "three_inside_up":          {"type": "bullish_reversal",      "reliability": "medium"},
    "bullish_harami":           {"type": "bullish_reversal",      "reliability": "medium"},
    "tweezer_bottom":           {"type": "bullish_reversal",      "reliability": "medium"},
    "bullish_counterattack":    {"type": "bullish_reversal",      "reliability": "low"},
    "bullish_kicker":           {"type": "bullish_reversal",      "reliability": "high"},
    "bullish_abandoned_baby":   {"type": "bullish_reversal",      "reliability": "high"},
    "morning_star_doji":        {"type": "bullish_reversal",      "reliability": "high"},
    "dragonfly_doji":           {"type": "bullish_reversal",      "reliability": "medium"},
    "bullish_tri_star":         {"type": "bullish_reversal",      "reliability": "low"},
    "bullish_hikkake":          {"type": "bullish_reversal",      "reliability": "medium"},
    "concealing_baby_swallow":  {"type": "bullish_reversal",      "reliability": "medium"},
    "unique_three_rivers":      {"type": "bullish_reversal",      "reliability": "low"},
    "rounding_bottom":          {"type": "bullish_continuation",  "reliability": "high"},
    "bullish_belt_hold":        {"type": "bullish_reversal",      "reliability": "medium"},
    "bullish_mat_hold":         {"type": "bullish_continuation",  "reliability": "high"},
    "rising_three_methods":     {"type": "bullish_continuation",  "reliability": "high"},
    "homing_pigeon":            {"type": "bullish_reversal",      "reliability": "medium"},
    "stick_sandwich":           {"type": "bullish_reversal",      "reliability": "medium"},
    "hanging_man":              {"type": "bearish_reversal",      "reliability": "high"},
    "dark_cloud_cover":         {"type": "bearish_reversal",      "reliability": "high"},
    "bearish_engulfing":        {"type": "bearish_reversal",      "reliability": "high"},
    "evening_star":             {"type": "bearish_reversal",      "reliability": "high"},
    "three_black_crows":        {"type": "bearish_continuation",  "reliability": "high"},
    "three_inside_down":        {"type": "bearish_reversal",      "reliability": "medium"},
    "bearish_harami":           {"type": "bearish_reversal",      "reliability": "medium"},
    "shooting_star":            {"type": "bearish_reversal",      "reliability": "high"},
    "tweezer_top":              {"type": "bearish_reversal",      "reliability": "medium"},
    "bearish_counterattack":    {"type": "bearish_reversal",      "reliability": "low"},
    "bearish_spinning_top":     {"type": "bearish_reversal",      "reliability": "low"},
    "bearish_kicker":           {"type": "bearish_reversal",      "reliability": "high"},
    "evening_star_doji":        {"type": "bearish_reversal",      "reliability": "high"},
    "bearish_abandoned_baby":   {"type": "bearish_reversal",      "reliability": "high"},
    "gravestone_doji":          {"type": "bearish_reversal",      "reliability": "medium"},
    "bearish_tri_star":         {"type": "bearish_reversal",      "reliability": "low"},
    "deliberation":             {"type": "bearish_reversal",      "reliability": "medium"},
    "upside_gap_two_crows":     {"type": "bearish_reversal",      "reliability": "medium"},
    "advance_block":            {"type": "bearish_reversal",      "reliability": "medium"},
    "rounding_top":             {"type": "bearish_continuation",  "reliability": "high"},
    "triple_top":               {"type": "bearish_reversal",      "reliability": "high"},
    "falling_three_methods":    {"type": "bearish_continuation",  "reliability": "high"},
    "on_neck":                  {"type": "bearish_continuation",  "reliability": "medium"},
    "in_neck":                  {"type": "bearish_continuation",  "reliability": "medium"},
}