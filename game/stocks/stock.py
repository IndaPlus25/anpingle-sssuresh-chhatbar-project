import random
import math
from .patterns import PATTERNS
from .metadata import PATTERN_META


class Candle:
    """Represents a single candlestick with OHLC data."""
    def __init__(self, open_price, high, low, close):
        self.open = open_price
        self.high = high
        self.low = low
        self.close = close
        self.tick = 0

    def update(self, price):
        """Update candle with new price tick."""
        self.tick += 1
        self.high = max(self.high, price)
        self.low = min(self.low, price)
        self.close = price

    def is_bullish(self):
        return self.close > self.open

    def is_bearish(self):
        return self.close < self.open

    def is_doji(self, threshold=0.001):
        """Check if candle is a doji (body very small relative to range)."""
        body = abs(self.close - self.open)
        range_ = self.high - self.low
        return range_ > 0 and body / range_ < threshold

    def __repr__(self):
        return f"Candle(open={self.open:.2f}, high={self.high:.2f}, low={self.low:.2f}, close={self.close:.2f})"


class Stock:
    def __init__(self, name, price, mu=0.0001, sigma=0.02, candles_per_tick=1):
        self.name = name
        self.price = float(price)
        self.mu = mu          # baseline drift per tick
        self.sigma = sigma    # volatility per tick
        self.history = [self.price]

        # Candlestick tracking
        self.candles = []
        self._current_candle = None
        self.candles_per_tick = candles_per_tick  # candles formed per GBM tick

        self.active_pattern = None  # (remaining_ticks, override_mu)

        self._pattern_queue = []
        self._active_segment = None
        self.current_pattern_name = None

        # Initialize first candle
        self._start_new_candle()

    def inject_pattern(self, ticks, drift, segments):
        """Force a directional drift for a number of ticks."""
        self._pattern_queue = [[ticks, drift] for ticks, drift in segments]
        self._active_segment = None
        self.current_pattern_name = None

    def inject_named_pattern(self, name):
        if name not in PATTERNS:
            available = ", ".join(sorted(PATTERNS.keys()))
            raise KeyError(
                f"unknown pattern '{name}'. Available patterns: {available}"
            )
        
        self.inject_pattern(*PATTERNS[name])
        self.current_pattern_name = name

    def get_pattern_meta(self, name=None):
        name = name or self.current_pattern_name
        if name is None:
            return None
        return PATTERN_META.get(name)
    
    def is_pattern_active(self):
        return self.active_pattern is not None or len(self._pattern_queue) > 0

    def _next_segment(self):
        if self._pattern_queue:
            self._active_segment = self._pattern_queue.pop(0)
        else:
            self._active_segment = None
            self.current_pattern_name = None
        

    def _start_new_candle(self):
        """Start a new candle using the previous candle's close or opening price."""
        if self.candles:
            open_price = self.candles[-1].close
        else:
            open_price = self.price
        self._current_candle = Candle(open_price, open_price, open_price, open_price)

    def finalize_candle(self):
        """Finalize the current candle and start a new one."""
        if self._current_candle is not None:
            self.candles.append(self._current_candle)
            self._current_candle = None
        self._start_new_candle()

    def update_price(self, record_candle=True):
        """Update price using GBM, optionally tracking candlestick data."""

        if self._active_segment is None and self._pattern_queue:
            self._next_segment()

        # Use pattern drift if active, else baseline
        if self._active_segment is not None:
            effective_mu = self._active_segment[1]
            self._active_segment[0] -= 1
            if self._active_segment[0] <= 0:
                self._next_segment()
        else:
            effective_mu = self.mu

        # GBM discrete step
        Z = random.gauss(0, 1)
        self.price *= math.exp(
            (effective_mu - 0.5 * self.sigma ** 2) + self.sigma * Z
        )

        self.price = max(0.01, round(self.price, 2))
        self.history.append(self.price)

        # Update current candle
        if record_candle and self._current_candle is not None:
            self._current_candle.update(self.price)

    def step(self, n=1):
        """Advance n ticks at once. Optionally finalize candles after steps."""
        for _ in range(n):
            self.update_price()

    def reset(self, price=None):
        if price is not None:
            self.price = float(price)

        self.history = [self.price]
        self.candles = []
        self._current_candle = None
        self._active_segment = None
        self._pattern_queue = []
        self.current_pattern_name = None

        # Initialize first candle
        self._start_new_candle()
    
    def __repr__(self):
        status = f"pattern= {self.current_pattern_name}" if self.is_pattern_active() else "no pattern"
        candle_count = len(self.candles)
        if self._current_candle:
            candle_count += 1

        return f"Stock({self.name!r}, price={self.price}, {status}, candles={candle_count})"