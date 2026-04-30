import random
import math
from .patterns import PATTERNS, PATTERN_META


class Stock:
    def __init__(self, name, price, mu=0.0001, sigma=0.02):
        self.name = name
        self.price = float(price)
        self.mu = mu          # baseline drift per tick
        self.sigma = sigma    # volatility per tick
        self.history = [self.price]
        self.active_pattern = None  # (remaining_ticks, override_mu)

        self._pattern_queue = []
        self._active_segment = None
        self.current_pattern_name = None

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
        

    def update_price(self):

        if self._active_segment is None and self._pattern_queue:
            self._next_segment()

        # Use pattern drift if active, else baseline
        if self._active_segment is not None:
            ticks_left, pattern_mu = self.active_pattern
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

    def step(self, n=1):
        """Advance n ticks at once."""
        for _ in range(n):
            self.update_price()

    def reset(self, price=None):
        if price is not None:
            self.price = float(price)
        
        self.history = [self.price]
        self._active_segment = None
        self._pattern_queue = []
        self.current_pattern_name = None
    
    def __repr__(self):
        status = f"pattern= {self.current_pattern_name}" if self.is_pattern_active() else "no pattern"

        return f"Stock({self.name!r}, price={self.price}, {status})"