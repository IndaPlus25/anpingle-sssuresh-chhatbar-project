import pygame
from .constants import GAME_W, GAME_H, DARK, GOLD, LGRAY, PANEL, WHITE, RED, GREEN, BLUE, GRAY, CHARACTERS
from features.interaction import draw_button

def draw_menu(game_surface, title_font, body_font, small_font, icon_play, icon_person, icon_quit):
    """Main menu screen"""
    game_surface.fill(DARK)
    
    # Draw Background Grid
    for x in range(0, GAME_W, 40): 
        pygame.draw.line(game_surface, (30, 30, 55), (x, 0), (x, GAME_H))
    for y in range(0, GAME_H, 40): 
        pygame.draw.line(game_surface, (30, 30, 55), (0, y), (GAME_W, y))

    # Titles
    title = title_font.render("HEDGE FUND", True, GOLD)
    sub   = body_font.render("The Game", True, LGRAY)
    game_surface.blit(title, title.get_rect(centerx=GAME_W // 2, y=120))
    game_surface.blit(sub,   sub.get_rect(centerx=GAME_W // 2,   y=200))
    pygame.draw.line(game_surface, GOLD, (460, 240), (820, 240), 2)

    # Buttons
    start_btn = pygame.Rect(490, 280, 300, 60)
    char_btn  = pygame.Rect(490, 360, 300, 60)
    quit_btn  = pygame.Rect(490, 440, 300, 60)

    # Draw Buttons
    draw_button(game_surface, start_btn, "START  (Enter)", small_font, color=(30, 140, 80), icon=icon_play)
    draw_button(game_surface, char_btn,  "Characters",     small_font, color=(60, 80, 160), icon=icon_person)
    draw_button(game_surface, quit_btn,  "Quit  (Q)",      small_font, color=(140, 40, 40), icon=icon_quit)

    return start_btn, char_btn, quit_btn

def draw_char_select(game_surface, title_font, body_font, small_font, selected_idx, all_anims, char_images):
    """Character select"""
    game_surface.fill(DARK)
    heading = title_font.render("SELECT CHARACTER", True, GOLD)
    game_surface.blit(heading, heading.get_rect(centerx=GAME_W // 2, y=60))

    card_w, card_h = 240, 340
    spacing = 40
    start_x = (GAME_W - (len(CHARACTERS) * card_w + (len(CHARACTERS)-1) * spacing)) // 2

    card_rects = []
    for i, char in enumerate(CHARACTERS):
        rect = pygame.Rect(start_x + i * (card_w + spacing), 160, card_w, card_h)
        card_rects.append(rect)
        
        # Highlight selected card
        bg = PANEL if i != selected_idx else (35, 55, 100)
        pygame.draw.rect(game_surface, bg, rect, border_radius=10)
        if i == selected_idx:
            pygame.draw.rect(game_surface, GOLD, rect, 2, border_radius=10)
        
        # Character Image
        display_img = None
        if i < len(all_anims) and all_anims[i]["idle"].get("south"):
            display_img = all_anims[i]["idle"]["south"]
        else:
            display_img = char_images[i]

        if display_img:
            img = pygame.transform.scale(display_img, (128, 128))
            game_surface.blit(img, img.get_rect(centerx=rect.centerx, y=180))
            
        name_surf = body_font.render(char["name"], True, WHITE if i == selected_idx else LGRAY)
        game_surface.blit(name_surf, name_surf.get_rect(centerx=rect.centerx, y=330))
        
        desc_surf = small_font.render(char["desc"], True, LGRAY)
        game_surface.blit(desc_surf, desc_surf.get_rect(centerx=rect.centerx, y=360))

    # Navigation Buttons
    back_btn = pygame.Rect(60, 620, 180, 50)
    confirm_btn = pygame.Rect(1040, 620, 180, 50)
    
    draw_button(game_surface, back_btn, "← Back", body_font, color=(80, 40, 80))
    draw_button(game_surface, confirm_btn, "Confirm ✓", body_font, color=(30, 140, 80))
    
    return card_rects, back_btn, confirm_btn

def draw_text_input(game_surface, rect, text, font, placeholder_font, is_active=False, placeholder="Enter amount..."):
    """Draws a text input field with the given text and optional cursor."""
    # Background
    bg_color = (30, 35, 55) if is_active else (20, 22, 42)
    border_color = GOLD if is_active else (60, 70, 90)
    pygame.draw.rect(game_surface, bg_color, rect, border_radius=6)
    pygame.draw.rect(game_surface, border_color, rect, 2, border_radius=6)

    # Text or placeholder
    if text:
        text_surf = font.render(text, True, WHITE)
    else:
        text_surf = placeholder_font.render(placeholder, True, (100, 100, 120))

    # Center the text
    text_rect = text_surf.get_rect(midleft=(rect.x + 12, rect.centery))
    game_surface.blit(text_surf, text_rect)

    # Draw cursor (blinking line) when active
    if is_active:
        cursor_x = text_rect.right + 2
        cursor_y = rect.y + 8
        cursor_height = rect.height - 16
        pygame.draw.line(game_surface, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

    return rect


# TEST
def draw_market_overlay(game_surface, body_font, hud_font, small_font, stocks,
                         selected_stock_idx=0, player_cash=0, player_portfolio=None,
                         amount_text="", input_active=False):
    """Draws the Stock Market interaction menu with candlestick charts and pattern info.

    Returns (left_arrow_rect, right_arrow_rect, buy_btn, sell_btn, amount_input_rect) for click-based stock navigation and trading.
    """
    from .constants import BLUE, GOLD, GREEN, GRAY, RED, WHITE, DARK
    from .assets.stock_assets import (
        CANDLE_COLORS, PATTERN_PROGRESS_BG, get_pattern_color, get_pattern_info,
        PATTERN_COLORS,
    )

    # --- layout constants ---
    BOX_W, BOX_H = 1020, 520
    box_x = (game_surface.get_width() - BOX_W) // 2
    box_y = (game_surface.get_height() - BOX_H) // 2
    box = pygame.Rect(box_x, box_y, BOX_W, BOX_H)

    # Semi-transparent dark overlay behind the panel
    overlay = pygame.Surface((game_surface.get_width(), game_surface.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    game_surface.blit(overlay, (0, 0))

    # Main panel
    pygame.draw.rect(game_surface, (10, 12, 28), box, border_radius=14)
    pygame.draw.rect(game_surface, BLUE, box, 2, border_radius=14)

    # --- Title ---
    title = body_font.render("STOCK MARKET", True, GOLD)
    game_surface.blit(title, (box.x + 30, box.y + 16))

    close_hint = small_font.render("Press Q to close  |  ← → to switch stocks", True, GRAY)
    game_surface.blit(close_hint, (box.x + BOX_W - close_hint.get_width() - 20, box.y + 22))

    # --- Stock selector strip (top row) ---
    strip_y = box.y + 55
    strip_h = 38
    strip_rect = pygame.Rect(box.x + 10, strip_y, BOX_W - 20, strip_h)
    pygame.draw.rect(game_surface, (18, 20, 40), strip_rect, border_radius=6)

    tab_w = max(80, (BOX_W - 60) // len(stocks))
    for i, s in enumerate(stocks):
        tx = box.x + 20 + i * tab_w
        tab_rect = pygame.Rect(tx, strip_y + 3, tab_w - 6, strip_h - 6)
        if i == selected_stock_idx:
            pygame.draw.rect(game_surface, (35, 55, 110), tab_rect, border_radius=5)
            pygame.draw.rect(game_surface, GOLD, tab_rect, 1, border_radius=5)
            tab_label = small_font.render(s.name, True, GOLD)
        else:
            tab_label = small_font.render(s.name, True, GRAY)
        game_surface.blit(tab_label, tab_label.get_rect(center=tab_rect.center))

    # Navigation arrows
    arrow_size = 28
    left_arrow_rect = pygame.Rect(box.x + 6, strip_y + 5, arrow_size, arrow_size)
    right_arrow_rect = pygame.Rect(box.x + BOX_W - arrow_size - 6, strip_y + 5, arrow_size, arrow_size)
    # (arrows are clickable but tabs already visible — draw subtle chevrons)
    arrow_font = body_font
    la = arrow_font.render("◀", True, GOLD)
    ra = arrow_font.render("▶", True, GOLD)
    game_surface.blit(la, la.get_rect(center=left_arrow_rect.center))
    game_surface.blit(ra, ra.get_rect(center=right_arrow_rect.center))

    # ----------------------------------------------------------------
    # Selected stock details
    # ----------------------------------------------------------------
    stock = stocks[selected_stock_idx]

    content_y = strip_y + strip_h + 14
    left_x = box.x + 30

    # --- Price header ---
    price_color = GREEN if (stock.candles and stock.price >= stock.candles[-1].close) else (
        RED if stock.candles else BLUE
    )
    price_text = f"${stock.price:.2f}"
    price_surf = hud_font.render(price_text, True, price_color)
    game_surface.blit(price_surf, (left_x, content_y))

    name_surf = hud_font.render(stock.name, True, WHITE)
    game_surface.blit(name_surf, (left_x + price_surf.get_width() + 16, content_y))

    # Change indicator
    if len(stock.history) >= 2:
        change = stock.price - stock.history[-2]
        pct = (change / stock.history[-2]) * 100 if stock.history[-2] != 0 else 0
        chg_str = f"{'▲' if change >= 0 else '▼'} {abs(change):.2f} ({abs(pct):.2f}%)"
        chg_color = GREEN if change >= 0 else RED
        chg_surf = small_font.render(chg_str, True, chg_color)
        game_surface.blit(chg_surf, (left_x, content_y + 28))

    candle_count_surf = small_font.render(f"Candles: {len(stock.candles)}", True, GRAY)
    game_surface.blit(candle_count_surf, (left_x + 250, content_y + 28))

    # ----------------------------------------------------------------
    # Candlestick chart
    # ----------------------------------------------------------------
    chart_x = left_x
    chart_y = content_y + 55
    chart_w = BOX_W - 120
    chart_h = 220
    chart_pad = 12

    # Candle colors
    light_green = CANDLE_COLORS["bullish"]["body"]
    dark_green  = CANDLE_COLORS["bullish"]["border"]
    light_red   = CANDLE_COLORS["bearish"]["body"]
    dark_red    = CANDLE_COLORS["bearish"]["border"]
    black       = (0, 0, 0)
    lgray       = (55, 55, 75)

    chart_rect = pygame.Rect(chart_x, chart_y, chart_w, chart_h)
    pygame.draw.rect(game_surface, (20, 22, 42), chart_rect, border_radius=6)
    pygame.draw.rect(game_surface, (50, 55, 80), chart_rect, 1, border_radius=6)

    candles = stock.candles
    if candles:
        candle_w = 8
        candle_sp = 3
        total_cw = candle_w + candle_sp
        max_vis = (chart_w - 2 * chart_pad - 50) // total_cw  # leave room for price axis
        visible = candles[-max_vis:]

        min_p = min(c.low for c in visible)
        max_p = max(c.high for c in visible)
        p_range = max_p - min_p
        if p_range == 0:
            p_range = 1

        avail_h = chart_h - 2 * chart_pad
        h_scale = avail_h / p_range

        def py(price):
            return chart_y + chart_pad + (max_p - price) * h_scale

        # Grid lines
        num_grid = 5
        for gi in range(num_grid + 1):
            gy = chart_y + chart_pad + (avail_h * gi // num_grid)
            pygame.draw.line(game_surface, lgray, (chart_x + chart_pad, gy),
                             (chart_x + chart_w - 50, gy), 1)
            grid_price = max_p - (p_range * gi / num_grid)
            pl = small_font.render(f"${grid_price:.1f}", True, GRAY)
            game_surface.blit(pl, (chart_x + chart_w - 48, gy - 6))

        # Draw candles
        cx = chart_x + chart_pad + 4
        for candle in visible:
            open_y = py(candle.open)
            close_y = py(candle.close)
            high_y = py(candle.high)
            low_y = py(candle.low)

            if candle.close >= candle.open:
                body_col = light_green
                bord_col = dark_green
            else:
                body_col = light_red
                bord_col = dark_red

            body_top = min(open_y, close_y)
            body_h = max(1, abs(close_y - open_y))

            # Wick
            wick_x = cx + candle_w // 2
            pygame.draw.line(game_surface, bord_col, (wick_x, int(high_y)),
                             (wick_x, int(low_y)), 1)
            # Body
            br = pygame.Rect(cx, int(body_top), candle_w, int(body_h))
            pygame.draw.rect(game_surface, body_col, br)
            pygame.draw.rect(game_surface, bord_col, br, 1)

            cx += total_cw
    else:
        no_data = small_font.render("Waiting for market data...", True, GRAY)
        game_surface.blit(no_data, no_data.get_rect(center=chart_rect.center))

    # ----------------------------------------------------------------
    # Pattern info panel (right side / below chart)
    # ----------------------------------------------------------------
    pattern_y = chart_y + chart_h + 14

    if stock.current_pattern_name:
        pinfo = get_pattern_info(stock.current_pattern_name)
        pcolor = get_pattern_color(stock.current_pattern_name) or GOLD

        if pinfo:
            display_name, category, _ = pinfo

            # Pattern badge
            badge_rect = pygame.Rect(left_x, pattern_y, 260, 28)
            pygame.draw.rect(game_surface, pcolor, badge_rect, border_radius=4)
            badge_text = small_font.render(f"  {display_name}", True, (255, 255, 255))
            game_surface.blit(badge_text, (badge_rect.x + 4, badge_rect.y + 4))

            cat_surf = small_font.render(category, True, GRAY)
            game_surface.blit(cat_surf, (left_x + 270, pattern_y + 4))

            # Progress bar
            bar_x = left_x + 420
            bar_w = 200
            bar_h = 14
            bar_y_pos = pattern_y + 6

            pygame.draw.rect(game_surface, PATTERN_PROGRESS_BG,
                             (bar_x, bar_y_pos, bar_w, bar_h), border_radius=3)
            pygame.draw.rect(game_surface, (80, 80, 100),
                             (bar_x, bar_y_pos, bar_w, bar_h), 1, border_radius=3)

            # Calculate progress
            total_ticks = getattr(stock, '_pattern_total_ticks', 20)
            remaining = 0
            if stock._active_segment:
                remaining += stock._active_segment[0]
            remaining += sum(seg[0] for seg in stock._pattern_queue)
            completed = max(0, total_ticks - remaining)
            progress = completed / total_ticks if total_ticks > 0 else 0

            fill_w = int(bar_w * progress)
            if fill_w > 0:
                pygame.draw.rect(game_surface, pcolor,
                                 (bar_x, bar_y_pos, fill_w, bar_h), border_radius=3)

            pct_text = small_font.render(f"{int(progress * 100)}%", True, WHITE)
            game_surface.blit(pct_text, (bar_x + bar_w + 8, bar_y_pos))
    else:
        idle_surf = small_font.render("No active pattern — market is drifting", True, GRAY)
        game_surface.blit(idle_surf, (left_x, pattern_y + 4))

    # ----------------------------------------------------------------
    # Trading panel (buy/sell)
    # ----------------------------------------------------------------
    trade_y = pattern_y + 50

    # Portfolio info
    owned_qty = 0
    if player_portfolio and stock.name in player_portfolio:
        owned_qty = player_portfolio[stock.name]

    portfolio_text = f"Owned: {owned_qty} shares"
    portfolio_surf = small_font.render(portfolio_text, True, (180, 180, 200))
    game_surface.blit(portfolio_surf, (left_x, trade_y))

    cash_text = f"Cash: ${player_cash:,.0f}"
    cash_surf = small_font.render(cash_text, True, GOLD)
    game_surface.blit(cash_surf, (left_x + 200, trade_y))

    # Amount input field - position it to fit within bounds
    input_x = left_x + 380
    input_y = pattern_y + 42
    input_w, input_h = 140, 34
    amount_input_rect = pygame.Rect(input_x, input_y, input_w, input_h)
    draw_text_input(game_surface, amount_input_rect, amount_text, small_font, small_font, input_active)

    # Buy/Sell buttons - aligned to bottom of input box
    btn_w, btn_h = 90, 32
    btn_y = input_y + input_h - btn_h  # Align bottom with input box

    buy_btn = pygame.Rect(input_x + input_w + 12, btn_y, btn_w, btn_h)
    buy_color = (30, 140, 80)  # Green
    if player_cash < stock.price or not amount_text:
        buy_color = (60, 80, 60)  # Dimmed green if can't afford
    draw_button(game_surface, buy_btn, "BUY", small_font, color=buy_color, radius=6)

    sell_btn = pygame.Rect(buy_btn.right + 10, btn_y, btn_w, btn_h)
    sell_color = (180, 60, 60)  # Red
    if owned_qty <= 0 or not amount_text:
        sell_color = (80, 60, 60)  # Dimmed red if can't sell
    draw_button(game_surface, sell_btn, "SELL", small_font, color=sell_color, radius=6)

    # ----------------------------------------------------------------
    # Stock ticker strip at the bottom
    # ----------------------------------------------------------------
    ticker_y = box.y + BOX_H - 36
    pygame.draw.line(game_surface, (40, 44, 65), (box.x + 10, ticker_y - 4),
                     (box.x + BOX_W - 10, ticker_y - 4), 1)

    tx = box.x + 20
    for s in stocks:

        col = GREEN if (s.candles and s.price >= s.candles[-1].close) else RED if s.candles else GRAY
        ticker_label = small_font.render(f"{s.name} ${s.price:.2f}", True, col)
        game_surface.blit(ticker_label, (tx, ticker_y))
        tx += ticker_label.get_width() + 20

    return left_arrow_rect, right_arrow_rect, buy_btn, sell_btn, amount_input_rect

def draw_shop_overlay(game_surface, body_font, small_font, player, icon_coin, thumbnails, owned_items, equipped_items, shop_tab, scroll_y):
    """Draws the shop overlay."""

    from .constants import BLUE, GOLD, GREEN, GRAY, PANEL, WHITE, SHOP_ITEMS
    
    win_w, win_h = 700, 500
    win_x, win_y = (game_surface.get_width() - win_w) // 2, (game_surface.get_height() - win_h) // 2
    box = pygame.Rect(win_x, win_y, win_w, win_h)
    
    # Draw Background
    pygame.draw.rect(game_surface, (40, 45, 60), box, border_radius=8)
    pygame.draw.rect(game_surface, PANEL, box.inflate(-10, -50), border_radius=4)
    
    title = body_font.render("Shop", True, WHITE)
    game_surface.blit(title, (box.x + 20, box.y + 10))
    
    close_btn = draw_close_button(game_surface, box.right - 50, box.y + 10, small_font)

    categories = ["Desks", "Walls", "Plants", "Upgrades"]
    tab_buttons = []
    tab_x = box.x + 150
    
    for cat in categories:
        tab_rect = pygame.Rect(tab_x, box.y + 15, 100, 30)
        is_active = (cat == shop_tab)
        bg_color = (60, 80, 160) if is_active else (50, 55, 75)
        text_color = WHITE if is_active else GRAY
        
        pygame.draw.rect(game_surface, bg_color, tab_rect, border_radius=4)
        if is_active:
            pygame.draw.rect(game_surface, GOLD, tab_rect, 1, border_radius=4)
            
        cat_text = small_font.render(cat, True, text_color)
        game_surface.blit(cat_text, cat_text.get_rect(center=tab_rect.center))
        
        tab_buttons.append({"rect": tab_rect, "category": cat})
        tab_x += 110

    filtered_items = [item for item in SHOP_ITEMS if item.get("category", "Desks") == shop_tab]
    list_rect = pygame.Rect(box.x + 10, box.y + 60, win_w - 20, win_h - 70)
    
    total_content_height = len(filtered_items) * 85
    max_scroll = min(0, list_rect.height - total_content_height - 20)
    
    if scroll_y > 0: scroll_y = 0
    if scroll_y < max_scroll: scroll_y = max_scroll

    game_surface.set_clip(list_rect)
    
    buy_buttons = []
    row_y = list_rect.y + 10 + scroll_y 
    
    for item in filtered_items:
        row_rect = pygame.Rect(win_x + 20, row_y, win_w - 40, 70)
        
        if row_rect.bottom > list_rect.top and row_rect.top < list_rect.bottom:
            pygame.draw.rect(game_surface, (35, 40, 55), row_rect, border_radius=6)
            pygame.draw.rect(game_surface, (50, 60, 80), row_rect, 1, border_radius=6)
            
            thumb = thumbnails.get(item["id"])
            if thumb: game_surface.blit(thumb, (row_rect.x + 10, row_rect.y + 5))
            
            name_text = small_font.render(item["name"], True, WHITE)
            game_surface.blit(name_text, (row_rect.x + 100, row_rect.y + 3))
            
            if icon_coin: game_surface.blit(icon_coin, (row_rect.x + 100, row_rect.y + 30))
            price_text = small_font.render(f"${item['price']:,}", True, GOLD)
            game_surface.blit(price_text, (row_rect.x + 140, row_rect.y + 33))
            
            btn_rect = pygame.Rect(row_rect.right - 140, row_rect.y + 15, 120, 40)
            is_owned = item["id"] in owned_items
            is_equipped = item["id"] == equipped_items.get(shop_tab)
            
            if is_equipped: btn_text, btn_color = "Equipped", GRAY
            elif is_owned: btn_text, btn_color = "Equip", BLUE
            else:
                can_afford = player.cash >= item["price"]
                btn_text, btn_color = "Buy", GREEN if can_afford else (140, 40, 40)
            
            draw_button(game_surface, btn_rect, btn_text, small_font, color=btn_color)
            buy_buttons.append((btn_rect, item, btn_text)) 
            
        row_y += 85 
        
    game_surface.set_clip(None) 
    
    # --- NEW: Return the perfectly clamped scroll_y and the close button rect ---
    return buy_buttons, tab_buttons, scroll_y, close_btn

def draw_confirmation_screen(game_surface, body_font, small_font, prompt_text):
    """yes/no"""
    overlay = pygame.Surface((game_surface.get_width(), game_surface.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) 
    game_surface.blit(overlay, (0, 0))

    # Center box
    box_w, box_h = 400, 200
    box_x = (game_surface.get_width() - box_w) // 2
    box_y = (game_surface.get_height() - box_h) // 2
    box = pygame.Rect(box_x, box_y, box_w, box_h)

    pygame.draw.rect(game_surface, (40, 45, 60), box, border_radius=8)
    pygame.draw.rect(game_surface, (200, 200, 220), box, 2, border_radius=8)

    # Text Prompt
    text_surf = body_font.render(prompt_text, True, (255, 255, 255))
    game_surface.blit(text_surf, text_surf.get_rect(centerx=box.centerx, y=box.y + 40))

    # Yes / No Buttons
    yes_btn = pygame.Rect(box_x + 50, box_y + 120, 120, 50)
    no_btn  = pygame.Rect(box_x + 230, box_y + 120, 120, 50)

    draw_button(game_surface, yes_btn, "Yes", small_font, color=(30, 140, 80))
    draw_button(game_surface, no_btn, "No", small_font, color=(140, 40, 40))

    return yes_btn, no_btn


def draw_staff_panel_overlay(game_surface, body_font, small_font, active_staff, available_employees, portraits):
    """Draws a professional Staff Management Panel with Shop and Management sections."""
    from .constants import BLUE, GOLD, GREEN, GRAY, RED, PANEL, WHITE
    
    # Main window
    win_w, win_h = 1100, 600
    win_x, win_y = (game_surface.get_width() - win_w) // 2, (game_surface.get_height() - win_h) // 2
    main_box = pygame.Rect(win_x, win_y, win_w, win_h)
    
    # Draw main background
    pygame.draw.rect(game_surface, (25, 28, 38), main_box, border_radius=12)
    pygame.draw.rect(game_surface, (60, 70, 90), main_box, 3, border_radius=12)
    
    # Header bar
    header_rect = pygame.Rect(win_x, win_y, win_w, 60)
    pygame.draw.rect(game_surface, (35, 40, 55), header_rect, border_top_left_radius=12, border_top_right_radius=12)
    pygame.draw.line(game_surface, (80, 90, 110), (win_x, win_y + 60), (win_x + win_w, win_y + 60), 2)
    
    # Title with icon
    title = body_font.render("⚡ STAFF MANAGEMENT", True, GOLD)
    game_surface.blit(title, (win_x + 30, win_y + 15))
    
    # Close hint
    close_hint = small_font.render("Press T to close", True, GRAY)
    game_surface.blit(close_hint, (win_x + win_w - close_hint.get_width() - 30, win_y + 20))
    
    # Split into 2 sections
    left_w = 520
    right_w = win_w - left_w - 60
    section_h = win_h - 90
    

    #Employee Shop

    left_x = win_x + 20
    left_y = win_y + 75
    left_box = pygame.Rect(left_x, left_y, left_w, section_h)
    
    pygame.draw.rect(game_surface, (30, 34, 45), left_box, border_radius=8)
    pygame.draw.rect(game_surface, (50, 60, 75), left_box, 2, border_radius=8)
    
    # Section title
    shop_title = small_font.render("📋 AVAILABLE FOR HIRE", True, WHITE)
    game_surface.blit(shop_title, (left_x + 15, left_y + 10))
    pygame.draw.line(game_surface, (60, 70, 85), (left_x + 10, left_y + 45), (left_x + left_w - 10, left_y + 45), 1)
    

    # Active Employees

    right_x = left_x + left_w + 20
    right_y = left_y
    right_box = pygame.Rect(right_x, right_y, right_w, section_h)
    
    pygame.draw.rect(game_surface, (30, 34, 45), right_box, border_radius=8)
    pygame.draw.rect(game_surface, (50, 60, 75), right_box, 2, border_radius=8)
    
    # Section title
    active_title = small_font.render("👥 ACTIVE STAFF", True, WHITE)
    game_surface.blit(active_title, (right_x + 15, right_y + 10))
    
    # Staff count badge
    staff_count = len(active_staff)
    badge_text = small_font.render(f"{staff_count}", True, WHITE)
    badge_rect = pygame.Rect(right_x + right_w - 50, right_y + 8, 35, 30)
    pygame.draw.rect(game_surface, GREEN if staff_count > 0 else GRAY, badge_rect, border_radius=15)
    game_surface.blit(badge_text, badge_text.get_rect(center=badge_rect.center))
    
    pygame.draw.line(game_surface, (60, 70, 85), (right_x + 10, right_y + 45), (right_x + right_w - 10, right_y + 45), 1)
    

    # RENDER SHOP EMPLOYEES
  
    staff_buttons = []
    shop_y = left_y + 60
    
    # Create smaller font for stats
    stat_font = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 18)
    btn_font = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 20)
    
    for emp in available_employees:
        emp_id = emp["id"]
        is_hired = emp_id in active_staff
        
        # Card style for each employee
        card_rect = pygame.Rect(left_x + 15, shop_y, left_w - 30, 110)
        
        # Background with different appearance for hired/available
        bg_color = (38, 42, 55) if not is_hired else (28, 32, 42)
        pygame.draw.rect(game_surface, bg_color, card_rect, border_radius=8)
        pygame.draw.rect(game_surface, (70, 80, 100) if not is_hired else (50, 55, 65), card_rect, 2, border_radius=8)
        
        # Portrait with frame
        port_rect = pygame.Rect(card_rect.x + 12, card_rect.y + 12, 60, 60)
        pygame.draw.rect(game_surface, (20, 24, 32), port_rect, border_radius=6)
        
        port = portraits.get(emp_id)
        if port:
            port_scaled = pygame.transform.scale(port, (56, 56))
            game_surface.blit(port_scaled, (port_rect.x + 2, port_rect.y + 2))
        
        # Employee name
        name_surf = small_font.render(emp["name"], True, WHITE if not is_hired else GRAY)
        game_surface.blit(name_surf, (card_rect.x + 85, card_rect.y + 12))
        
        # Stats row 1: Energy & Speed
        stats_y = card_rect.y + 42
        
        # Energy stat with icon
        energy_label = stat_font.render("⚡", True, GOLD)
        game_surface.blit(energy_label, (card_rect.x + 85, stats_y))
        
        energy_text = stat_font.render(f"{emp['max_energy']}", True, (200, 200, 200))
        game_surface.blit(energy_text, (card_rect.x + 110, stats_y))
        
        # Speed stat with icon
        speed_label = stat_font.render("🚀", True, BLUE)
        game_surface.blit(speed_label, (card_rect.x + 180, stats_y))
        
        speed_text = stat_font.render(f"{emp['effectiveness']}x", True, (200, 200, 200))
        game_surface.blit(speed_text, (card_rect.x + 210, stats_y))
        
        # Salary badge
        salary_rect = pygame.Rect(card_rect.x + 85, card_rect.y + 68, 160, 28)
        pygame.draw.rect(game_surface, (45, 50, 65), salary_rect, border_radius=5)
        
        sal_text = stat_font.render(f"💰 ${emp['salary']}/hr", True, GOLD)
        game_surface.blit(sal_text, (salary_rect.x + 8, salary_rect.y + 5))
        
        # Hire button
        hire_btn = pygame.Rect(card_rect.right - 95, card_rect.y + 35, 80, 40)
        
        if is_hired:
            btn_color = (60, 60, 70)
            btn_text = "HIRED"
            text_color = GRAY
        else:
            btn_color = (40, 150, 80)
            btn_text = "HIRE"
            text_color = WHITE
        
        draw_button(game_surface, hire_btn, btn_text, btn_font, color=btn_color, radius=6)
        
        staff_buttons.append({
            "id": emp_id, 
            "hire_rect": hire_btn, 
            "fire_rect": pygame.Rect(0, 0, 0, 0),  # Will set for active staff
            "config": emp
        })
        
        shop_y += 125
    active_y = right_y + 60
    
    if len(active_staff) == 0:
        # Empty state
        empty_text = small_font.render("No active employees", True, GRAY)
        game_surface.blit(empty_text, empty_text.get_rect(centerx=right_box.centerx, y=active_y + 100))
        
        hint_text = stat_font.render("Hire staff from the left panel", True, GRAY)
        game_surface.blit(hint_text, hint_text.get_rect(centerx=right_box.centerx, y=active_y + 130))
    else:
        for emp_id, emp_npc in active_staff.items():
            emp_config = emp_npc.config
            
            # Compact card for active employees
            active_card = pygame.Rect(right_x + 15, active_y, right_w - 30, 90)
            
            pygame.draw.rect(game_surface, (38, 42, 55), active_card, border_radius=8)
            pygame.draw.rect(game_surface, (60, 140, 80), active_card, 2, border_radius=8)
            
            # Portrait
            port_rect_active = pygame.Rect(active_card.x + 10, active_card.y + 10, 50, 50)
            pygame.draw.rect(game_surface, (20, 24, 32), port_rect_active, border_radius=6)
            
            port = portraits.get(emp_id)
            if port:
                port_scaled = pygame.transform.scale(port, (46, 46))
                game_surface.blit(port_scaled, (port_rect_active.x + 2, port_rect_active.y + 2))
            
            # Name
            name_surf = btn_font.render(emp_config["name"], True, WHITE)
            game_surface.blit(name_surf, (active_card.x + 70, active_card.y + 10))
            
            # Energy bar with label
            energy_y = active_card.y + 38
            energy_label = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16).render("Energy:", True, LGRAY)
            game_surface.blit(energy_label, (active_card.x + 70, energy_y))
            
            bar_x = active_card.x + 145
            bar_w, bar_h = 180, 18
            pygame.draw.rect(game_surface, (20, 24, 32), (bar_x, energy_y, bar_w, bar_h), border_radius=4)
            pygame.draw.rect(game_surface, (60, 65, 75), (bar_x, energy_y, bar_w, bar_h), 1, border_radius=4)
            
            # Energy fill with dynamic color
            fill_pct = max(0, min(1, emp_npc.energy / emp_npc.max_energy))
            if fill_pct > 0:
                bar_color = GREEN if fill_pct > 0.5 else (255, 180, 0) if fill_pct > 0.25 else RED
                fill_w = int(bar_w * fill_pct)
                pygame.draw.rect(game_surface, bar_color, (bar_x, energy_y, fill_w, bar_h), border_radius=4)
            
            # Energy text overlay
            energy_text = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16).render(
                f"{int(emp_npc.energy)}/{emp_npc.max_energy}", True, WHITE
            )
            game_surface.blit(energy_text, energy_text.get_rect(center=(bar_x + bar_w // 2, energy_y + bar_h // 2)))
            
            # Speed indicator
            speed_y = active_card.y + 62
            speed_icon = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16).render(
                f"🚀 Speed: {emp_config['effectiveness']}x", True, BLUE
            )
            game_surface.blit(speed_icon, (active_card.x + 70, speed_y))
            
            # Fire button
            fire_btn = pygame.Rect(active_card.right - 80, active_card.y + 25, 65, 35)
            draw_button(game_surface, fire_btn, "FIRE", 
                       pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 18), 
                       color=(180, 40, 50), radius=6)
            
            # Update fire_rect for this employee
            for btn in staff_buttons:
                if btn["id"] == emp_id:
                    btn["fire_rect"] = fire_btn
                    break
            
            active_y += 100
    
    return staff_buttons
def draw_news_screen(game_surface, title_font, body_font, small_font, news_items, scroll_offset=0):
    """
    News feed screen showing stock-related headlines.
    
    news_items: list of dicts with keys:
        - headline (str)
        - summary (str)
        - ticker (str)        e.g. "AAPL"
        - impact (str)        "positive" | "negative" | "neutral"
        - timestamp (str)     e.g. "Day 4, 09:30"
    
    Returns: list of (rect, news_item) tuples for click detection
    """
    from .constants import BLUE, GOLD, GREEN, GRAY, RED

    game_surface.fill(DARK)

    # Background grid (matches menu style)
    for x in range(0, GAME_W, 40):
        pygame.draw.line(game_surface, (30, 30, 55), (x, 0), (x, GAME_H))
    for y in range(0, GAME_H, 40):
        pygame.draw.line(game_surface, (30, 30, 55), (0, y), (GAME_W, y))

    # Header bar
    header_rect = pygame.Rect(0, 0, GAME_W, 100)
    pygame.draw.rect(game_surface, PANEL, header_rect)
    pygame.draw.line(game_surface, GOLD, (0, 100), (GAME_W, 100), 2)

    heading = title_font.render("MARKET NEWS", True, GOLD)
    game_surface.blit(heading, heading.get_rect(centerx=GAME_W // 2, y=20))

    #sub = small_font.render("Live feed — click a story to expand", True, LGRAY)
    #game_surface.blit(sub, sub.get_rect(centerx=GAME_W // 2, y=68))

    # Back button
    back_btn = pygame.Rect(40, 25, 160, 50)
    draw_button(game_surface, back_btn, "← Back", body_font, color=(80, 40, 80))

    # News cards
    IMPACT_COLORS = {
        "positive": (30, 160, 80),
        "negative": (180, 45, 45),
        "neutral":  (80, 100, 160),
    }

    card_w    = GAME_W - 160
    card_h    = 110
    card_x    = 80
    start_y   = 120
    gap       = 18

    card_rects = []

    for i, item in enumerate(news_items):
        card_y = start_y + i * (card_h + gap) - scroll_offset
        # Skip cards fully outside the visible area
        if card_y + card_h < start_y or card_y > GAME_H:
            card_rects.append((None, item))
            continue

        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

        # Card background
        pygame.draw.rect(game_surface, (22, 26, 48), card_rect, border_radius=8)

        # Left accent stripe for impact
        impact_col = IMPACT_COLORS.get(item.get("impact", "neutral"), LGRAY)
        stripe = pygame.Rect(card_x, card_y, 6, card_h)
        pygame.draw.rect(game_surface, impact_col, stripe,
                         border_radius=4)

        # Card border
        pygame.draw.rect(game_surface, (50, 60, 90), card_rect, 1, border_radius=8)

        # Ticker badge
        ticker_text = item.get("ticker", "???")
        badge_surf  = small_font.render(f" {ticker_text} ", True, DARK)
        badge_rect  = badge_surf.get_rect(x=card_x + 20, y=card_y + 14)
        badge_bg    = badge_rect.inflate(8, 4)
        pygame.draw.rect(game_surface, impact_col, badge_bg, border_radius=4)
        game_surface.blit(badge_surf, badge_rect)

        # Headline
        headline_surf = body_font.render(item.get("headline", ""), True, WHITE)
        game_surface.blit(headline_surf, (card_x + badge_bg.right - card_x + 16, card_y + 12))

        # Summary (truncated)
        summary = item.get("summary", "")
        if len(summary) > 90:
            summary = summary[:87] + "..."
        summary_surf = small_font.render(summary, True, LGRAY)
        game_surface.blit(summary_surf, (card_x + 20, card_y + 52))

        # Timestamp (bottom-right)
        ts_surf = small_font.render(item.get("timestamp", ""), True, (90, 100, 130))
        game_surface.blit(ts_surf, ts_surf.get_rect(right=card_rect.right - 16,
                                                     bottom=card_rect.bottom - 10))

        # "Read more" hint (bottom-right, before timestamp)
        hint_surf = small_font.render("Click to expand ›", True, (70, 90, 140))
        game_surface.blit(hint_surf, hint_surf.get_rect(right=card_rect.right - 16,
                                                         y=card_y + 52))

        card_rects.append((card_rect, item))

    # Scroll hint if there's more content below
    total_h = len(news_items) * (card_h + gap)
    if total_h > GAME_H - start_y:
        hint = small_font.render("↑ ↓  Scroll for more", True, (70, 80, 110))
        game_surface.blit(hint, hint.get_rect(centerx=GAME_W // 2, y=GAME_H - 28))

    return back_btn, card_rects


def draw_news_detail(game_surface, title_font, body_font, small_font, item):
    from .constants import GOLD, GREEN, GRAY

    IMPACT_COLORS = {
        "positive": (30, 160, 80),
        "negative": (180, 45, 45),
        "neutral":  (80, 100, 160),
    }
    impact_col = IMPACT_COLORS.get(item.get("impact", "neutral"), LGRAY)

    # Dim the background
    overlay = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    game_surface.blit(overlay, (0, 0))

    # Panel
    pan_w, pan_h = 860, 620
    pan_x = (GAME_W - pan_w) // 2
    pan_y = (GAME_H - pan_h) // 2
    panel = pygame.Rect(pan_x, pan_y, pan_w, pan_h)

    pygame.draw.rect(game_surface, (18, 22, 42), panel, border_radius=12)
    pygame.draw.rect(game_surface, impact_col, pygame.Rect(pan_x, pan_y, pan_w, 6), border_radius=12)
    pygame.draw.rect(game_surface, (55, 65, 100), panel, 2, border_radius=12)

    # Ticker badge + impact label
    badge_surf = body_font.render(f" {item.get('ticker', '???')} ", True, (10, 10, 20))
    badge_rect = badge_surf.get_rect(x=pan_x + 30, y=pan_y + 26)
    badge_bg   = badge_rect.inflate(12, 6)
    pygame.draw.rect(game_surface, impact_col, badge_bg, border_radius=5)
    game_surface.blit(badge_surf, badge_rect)
    game_surface.blit(
        small_font.render(item.get("impact", "neutral").upper(), True, impact_col),
        (badge_bg.right + 14, pan_y + 32)
    )

    # Timestamp
    ts_surf = small_font.render(item.get("timestamp", ""), True, (90, 100, 130))
    game_surface.blit(ts_surf, ts_surf.get_rect(right=panel.right - 24, y=pan_y + 32))

    # Divider
    pygame.draw.line(game_surface, (40, 50, 80), (pan_x + 20, pan_y + 72), (pan_x + pan_w - 20, pan_y + 72), 1)

    # --- Dynamic stacking starts here ---
    y = pan_y + 84

    # Headline
    game_surface.blit(body_font.render(item.get("headline", ""), True, WHITE), (pan_x + 30, y))
    y += body_font.get_linesize() + 8

    # Summary
    game_surface.blit(small_font.render(item.get("summary", ""), True, LGRAY), (pan_x + 30, y))
    y += small_font.get_linesize() + 12

    # Divider
    pygame.draw.line(game_surface, (40, 50, 80), (pan_x + 20, y), (pan_x + pan_w - 20, y), 1)
    y += 12

    # Body text with word wrap
    max_width = pan_w - 60
    words = item.get("body", "No further details available.").split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        if small_font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    for line in lines:
        if y > pan_y + pan_h - 100:
            break
        game_surface.blit(small_font.render(line, True, (190, 200, 220)), (pan_x + 30, y))
        y += small_font.get_linesize()

    # Related tickers
    related = item.get("related", [])
    if related:
        pygame.draw.line(game_surface, (40, 50, 80),
                         (pan_x + 20, pan_y + pan_h - 90),
                         (pan_x + pan_w - 20, pan_y + pan_h - 90), 1)
        game_surface.blit(small_font.render("Related:", True, LGRAY), (pan_x + 30, pan_y + pan_h - 72))
        rx = pan_x + 110
        for ticker in related:
            t_surf = small_font.render(ticker, True, DARK)
            t_rect = t_surf.get_rect(x=rx, y=pan_y + pan_h - 74)
            bg     = t_rect.inflate(12, 6)
            pygame.draw.rect(game_surface, (60, 100, 180), bg, border_radius=4)
            game_surface.blit(t_surf, t_rect)
            rx = bg.right + 10

    # Close button
    close_btn = pygame.Rect(panel.right - 150, panel.bottom - 60, 120, 40)
    draw_button(game_surface, close_btn, "✕  Close", small_font, color=(120, 40, 40))

    return close_btn
def draw_close_button(game_surface, x, y, font):
    """Draws a red rectangular close button with an X."""
    btn_rect = pygame.Rect(x, y, 40, 40)
    pygame.draw.rect(game_surface, (180, 50, 50), btn_rect, border_radius=6)
    pygame.draw.rect(game_surface, (255, 100, 100), btn_rect, 2, border_radius=6)
    
    x_text = font.render("X", True, (255, 255, 255))
    # Push the X slightly up/down depending on your font so it centers perfectly
    game_surface.blit(x_text, x_text.get_rect(center=btn_rect.center))
    
    return btn_rect
