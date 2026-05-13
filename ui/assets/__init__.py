"""Visual assets for candlestick patterns - defines colors and visual styles."""

from . import stock_assets

# Backward-compatible aliases so existing ``from ui.assets import patterns``
# or ``from ui.assets import candles`` style imports keep working.
patterns = stock_assets
candles = stock_assets

__all__ = ['stock_assets', 'patterns', 'candles']
