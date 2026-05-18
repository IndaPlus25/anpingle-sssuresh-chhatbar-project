# anpingle-sssuresh-chhatbar-project

# 📊 Hedge Fund: The Game

A real-time, fast-paced single-player corporate simulation game built in Python using **Pygame**. Step into the shoes of an ambitious fund manager juggling live market trading context, candlestick technical analysis patterns, office customization, employee recruitment, and tax-evading offshore wire maneuvers—all while avoiding catastrophic audits from the IRS.

---

## 🚀 Key Features

* **Dynamic Candlestick Stock Market:** Trade a variety of volatile stocks. Features high-performance candlestick charts rendering open, high, low, and close (OHLC) values alongside moving gridlines and animated real-time stock ticker banners.
* **Automated Pattern Recognition:** Tracks live asset trend lines to automatically inject and trace technical analysis chart formations (e.g., *Head and Shoulders*, *Double Bottoms*, etc.) complete with progression indicators.
* **Staff Recruitment & Management Panels:** Hire employees from an asset roster pool. Assign distinct occupational roles (e.g., *Salesmen* to aggressively secure liquid cash flows, *Accountants* to smoothly optimize baseline legal tax liabilities). Employees have dynamic stamina decay systems and sleep states.
* **Offshore Accounts & Auditing Risk (IRS):** Evade financial liabilities by physically holding space near your terminal desk to transfer your liquid cash into protected offshore assets. Face active structural IRS Agent sweeps that issue devastating **250% SEC fines** if you are caught wiring funds mid-audit.
* **Office Furnishing Shop:** Spend your hard-earned trading profits to upgrade your office space across multiple categorized layout tiers (`Desks`, `Walls`, `Plants`, `Upgrades`), with support for customizable grid placeables.
* **Dynamic Lighting Day/Night Engine:** Office lighting shifts seamlessly over smooth multi-phase transition curves (*Day*, *Sunset*, *Night*, *Sunrise*) complete with circular warm light auras casting from both the player and active glowing computer monitors.
* **Widescreen Framebuffer Pipeline:** Built on an insulated high-performance low-resolution rendering canvas canvas size (`GAME_W` x `GAME_H`) which automatically scales using an optimized anti-aliasing pixel scaler to match any native monitor fullscreen viewport setup.
* **Insulated Configuration Settings Window:** Seamless overlay architecture housing immediate, hardware-level audio track mixer slider controls (`Music Volume`, `SFX Volume`), brightness gamma overlays, and interactive manuals.

---

## 🎮 Extended Controls Manual

| Input | Target Panel / Context Action |
| :--- | :--- |
| **`W`, `A`, `S`, `D` / Arrows** | Character Movement / Adjust Grid Placement Previews |
| **`E`** | Interact with Computer Desk (Opens Main Stock Market Window) |
| **`TAB`** | Toggle Office Furnishing Upgrade Shop |
| **`T`** | Open Staff Management & Recruitment Panel |
| **`P`** | Toggle Personal Portfolio Tracker, Holdings, & Historical P&L |
| **`N`** | Open Live Breaking News Feed |
| **`B`** | Accounts and Tax Liability |
| **`SPACEBAR` (Hold)** | Execute Emergency Asset Transfer to Offshore Accounts |
| **`ENTER`** | Menu Confirmation / Lock Custom Placed Shop Item |
| **`ESC`** | Toggle Global Settings Window / Force-Close Active Interface Layer |
| **`Q`** | Force Exit / Close Current Trading Desk Overlay Menu |
| **`Mouse Click`** | Button Interactivity, Slider Controls, and Context Tabs |

---

## 📂 Project Architecture

```text
├── main.py                    # Game launch orchestration bootstrap hook
├── ui/
│   ├── pygame.py              # Main Engine Loop, Hardware Input, Event Routers, Game Context State
│   ├── screens.py             # Render Pipeline Layouts (Overlays, Settings, Portfolio, Shops)
│   ├── constants.py           # Global resolution metrics, screen flags, asset mapping specs
│   └── assets/
│       ├── music/             # CD-quality audio tracks, loop buffers, hardware mixing configurations
│       └── stock_assets.py    # Color aliases, grid configs, trendline calculations
├── features/
│   ├── assets.py              # Asset loaders (Spritesheets, textures, audio configurations)
│   ├── clock.py               # Time keeping context tracking simulation cycles
│   ├── hud.py                 # Persistent UI balance readouts, animated ticker ribbons
│   ├── irs.py                 # IRS agent movement pathways, speech indicators, warning assets
│   ├── npc.py                 # Employee NPCs behavioral routines, energy tracking, role traits
│   ├── placement.py           # Custom placeable grid boundary validation calculations
│   └── player.py              # Physics handlers, velocity matrices, animation trackers
└── game/
    ├── news.py                # Narrative breaking story string generators
    └── stocks/
        └── patterns.py        # Trend pattern injection dictionaries