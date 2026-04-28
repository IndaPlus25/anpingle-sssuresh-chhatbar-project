import random
import math

class Stock:
    def __init__(self, name, price, mu=0.0001, sigma=0.02):
        self.name = name
        self.price = float(price)
        self.mu = mu          # baseline drift per tick
        self.sigma = sigma    # volatility per tick
        self.history = [self.price]
        self.active_pattern = None  # (remaining_ticks, override_mu)

    def inject_pattern(self, ticks, drift_override):
        """Force a directional drift for a number of ticks."""
        self.active_pattern = [ticks, drift_override]

    def update_price(self):
        # Use pattern drift if active, else baseline
        if self.active_pattern:
            ticks_left, pattern_mu = self.active_pattern
            effective_mu = pattern_mu
            self.active_pattern[0] -= 1
            if self.active_pattern[0] <= 0:
                self.active_pattern = None
        else:
            effective_mu = self.mu

        # GBM discrete step
        dt = 1
        Z = random.gauss(0, 1)
        self.price *= math.exp((effective_mu - 0.5 * self.sigma**2) * dt
                               + self.sigma * math.sqrt(dt) * Z)

        self.price = max(0.01, round(self.price, 2))
        self.history.append(self.price)

    def step(self, n=1):
        """Advance n ticks at once."""
        for _ in range(n):
            self.update_price()