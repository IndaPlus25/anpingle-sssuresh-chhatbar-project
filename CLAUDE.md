# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Hedge Fund Trading Game** built with Python and Pygame. It simulates a stock market environment where players control a character that can move around and interact with a stock market interface.

## Architecture

### Core Structure

```
├── main.py              # Entry point: initializes Game and runs the UI
├── game/
│   ├── game.py          # Game class: manages players and stocks
│   ├── player.py        # Player class: manages player state and movement
│   └── stocks/
│       ├── stock.py     # Stock class: GBM price simulation with patterns
│       ├── patterns.py  # 48 trading patterns (bullish/bearish, reversal/continuation)
│       └── metadata.py  # Pattern metadata for UI/quiz logic
└── ui/
    └── pygame.py        # Pygame UI: rendering, input handling, game loop
```

### Key Components

**Game Logic** (`game/`):
- `Game`: Orchestrates players and stocks array
- `Player`: Has cash ($1M), portfolio dict, and x/y coordinates for movement
- `Stock`: Uses Geometric Brownian Motion (GBM) with pattern injection support

**Stock Pattern System** (`game/stocks/`):
- 48 trading patterns defined in `patterns.py` (e.g., `HAMMER`, `BULLISH_ENGULFING`, `THREE_BLACK_CROWS`)
- Patterns are `list[ticks, drift]` tuples injected into the GBM engine
- Patterns affect price over multiple ticks for realistic candlestick formation
- `PATTERN_META` in `metadata.py` provides pattern classification (bullish/bearish, reliability)

**UI** (`ui/pygame.py`):
- 600x400 window with Pygame
- Player movement (A/D keys) when market is closed
- Press E near computer to open market
- Press Q to close market and see stock prices

## Development Commands

```bash
# Run the game
python3 main.py

# Install dependencies (if needed)
pip3 install pygame
```

## Testing

No test suite exists yet. Test files would follow standard Python naming: `test_*.py` or `*_test.py`.

