# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Hedge Fund Trading Game** - A Pygame-based trading simulation where players control a character in a trading office environment and interact with a stock market interface. Stock prices use Geometric Brownian Motion (GBM) with 48 candlestick trading patterns.

## Architecture

```
├── main.py              # Entry point with assets loading and main loop
├── game/
│   ├── game.py          # Game class managing players and stocks array
│   ├── player.py        # Player class with x/y movement and direction
│   └── stocks/
│       ├── stock.py     # Stock class with GBM price simulation
│       ├── patterns.py  # 48 trading patterns (list of ticks+drift tuples)
│       └── metadata.py  # Pattern metadata for UI classification
├── ui/
│   ├── constants.py     # Screen dimensions (1280x720), colors, character defs
│   ├── screens.py       # Menu, character select, market/shop overlays
│   ├── pygame.py        # Main game loop and rendering
│   └── fonts/           # Pixelify Sans font files
├── features/
│   ├── player.py        # Movement handling (WASD), 8-directional
│   ├── interaction.py   # Mouse interaction with scaled coordinates
│   ├── hud.py           # Top bar with cash, stock ticker, menu button
│   ├── assets.py        # Asset loader (fonts, images, animations)
│   └── animations.py    # 8-way directional animation loader
└── assets/
    └── candlestick_assets/
        └── stock_assets.py  # Consolidated candle rendering + pattern labels/colors
```

## Key Components

**Game Loop** (`main.py`):
- Loads all assets from `features/assets.py`
- Main event loop handles keyboard (WASD, E for market, Q to close)
- Updates stocks every 1000ms (1 second)

**Stock Pattern System** (`game/stocks/`):
- 48 trading patterns defined in `patterns.py`
- Patterns are `list[ticks, drift]` tuples injected into GBM engine
- Drift values override the baseline `mu` parameter during pattern formation
- Categories: bullish/bearish reversal or continuation

**UI System**:
- 1280x720 window with scaled mouse coordinates
- 8-directional character animations (north, south, east, west, NE, NW, SE, SW)
- Shop system with desk upgrades (5 tiers up to $50,000)
- Stock market overlay with candlestick charts

## Development Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run the game
python3 main.py
```

## Dependencies

- Python 3.12
- Pygame 2.6.1

## Common Tasks

**Adding a new pattern**: Define the segment list in `game/stocks/patterns.py` and add to the `PATTERNS` registry.

**Adding a new shop item**: Update `ui/constants.py` `SHOP_ITEMS` list with id, name, price, and file path.

**Modifying character animations**: Update `features/animations.py` - expects 8-directional idle/walk PNG files.
