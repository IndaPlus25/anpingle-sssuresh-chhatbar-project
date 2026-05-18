import pygame
from .constants import GAME_W, GAME_H, DARK, GOLD, LGRAY, PANEL, WHITE, RED, GREEN, BLUE, GRAY, CHARACTERS
from features.interaction import draw_button

def draw_menu(game_surface, title_font, body_font, small_font, icon_play, icon_person, icon_quit):
    game_surface.fill(DARK)
    for x in range(0, GAME_W, 40): 
        pygame.draw.line(game_surface, (30, 30, 55), (x, 0), (x, GAME_H))
    for y in range(0, GAME_H, 40): 
        pygame.draw.line(game_surface, (30, 30, 55), (0, y), (GAME_W, y))
    title = title_font.render("HEDGE FUND", True, GOLD)
    sub   = body_font.render("The Game", True, LGRAY)
    game_surface.blit(title, title.get_rect(centerx=GAME_W // 2, y=120))
    game_surface.blit(sub,   sub.get_rect(centerx=GAME_W // 2,   y=200))
    pygame.draw.line(game_surface, GOLD, (460, 240), (820, 240), 2)
    start_btn = pygame.Rect(490, 280, 300, 60)
    char_btn  = pygame.Rect(490, 360, 300, 60)
    quit_btn  = pygame.Rect(490, 440, 300, 60)
    draw_button(game_surface, start_btn, "START  (Enter)", small_font, color=(30, 140, 80), icon=icon_play)
    draw_button(game_surface, char_btn,  "Characters",     small_font, color=(60, 80, 160), icon=icon_person)
    draw_button(game_surface, quit_btn,  "Quit  (Q)",      small_font, color=(140, 40, 40), icon=icon_quit)
    return start_btn, char_btn, quit_btn


def draw_char_select(game_surface, title_font, body_font, small_font, selected_idx, all_anims, char_images):
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
        bg = PANEL if i != selected_idx else (35, 55, 100)
        pygame.draw.rect(game_surface, bg, rect, border_radius=10)
        if i == selected_idx:
            pygame.draw.rect(game_surface, GOLD, rect, 2, border_radius=10)
        display_img = None
        if i < len(all_anims) and all_anims[i]["idle"].get("south"):
            display_img = all_anims[i]["idle"]["south"]
        else:
            display_img = char_images[i]
        if display_img:
            img = pygame.transform.scale(display_img, (128, 128))
            game_surface.blit(img, img.get_rect(centerx=rect.centerx, y=180))
        game_surface.blit(body_font.render(char["name"], True, WHITE if i == selected_idx else LGRAY),
                          body_font.render(char["name"], True, WHITE).get_rect(centerx=rect.centerx, y=330))
        game_surface.blit(small_font.render(char["desc"], True, LGRAY),
                          small_font.render(char["desc"], True, LGRAY).get_rect(centerx=rect.centerx, y=360))
    back_btn    = pygame.Rect(60,   620, 180, 50)
    confirm_btn = pygame.Rect(1040, 620, 180, 50)
    draw_button(game_surface, back_btn,    "← Back",    body_font, color=(80, 40, 80))
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
                         player_shorts=None,
                         amount_text="", input_active=False, ticker_offset=0):
    """Draws the Stock Market interaction menu with candlestick charts and pattern info.
    Returns (left_arrow_rect, right_arrow_rect, buy_btn, short_btn, amount_input_rect, close_btn).
    """
    from .constants import BLUE, GOLD, GREEN, GRAY, RED, WHITE, DARK
    from .assets.stock_assets import CANDLE_COLORS, PATTERN_PROGRESS_BG, get_pattern_color, get_pattern_info, PATTERN_COLORS

    # Increased box height to 600 for plenty of room
    BOX_W, BOX_H = 1020, 600 
    box_x = (game_surface.get_width()  - BOX_W) // 2
    box_y = (game_surface.get_height() - BOX_H) // 2
    box   = pygame.Rect(box_x, box_y, BOX_W, BOX_H)

    overlay = pygame.Surface((game_surface.get_width(), game_surface.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    game_surface.blit(overlay, (0, 0))

    pygame.draw.rect(game_surface, (10, 12, 28), box, border_radius=14)
    pygame.draw.rect(game_surface, BLUE, box, 2, border_radius=14)

    game_surface.blit(body_font.render("STOCK MARKET", True, GOLD), (box.x + 30, box.y + 16))
    
    # --- NEW: Draw the professional Close Button instead of text hints ---
    close_btn = draw_close_button(game_surface, box.right - 50, box.y + 12, small_font)

    strip_y = box.y + 55
    strip_h = 38
    pygame.draw.rect(game_surface, (18, 20, 40), pygame.Rect(box.x + 10, strip_y, BOX_W - 20, strip_h), border_radius=6)

    tab_w = max(80, (BOX_W - 60) // len(stocks))
    for i, s in enumerate(stocks):
        tab_rect = pygame.Rect(box.x + 20 + i * tab_w, strip_y + 3, tab_w - 6, strip_h - 6)
        if i == selected_stock_idx:
            pygame.draw.rect(game_surface, (35, 55, 110), tab_rect, border_radius=5)
            pygame.draw.rect(game_surface, GOLD, tab_rect, 1, border_radius=5)
            tab_label = small_font.render(s.name, True, GOLD)
        else:
            tab_label = small_font.render(s.name, True, GRAY)
        game_surface.blit(tab_label, tab_label.get_rect(center=tab_rect.center))

    arrow_size       = 28
    left_arrow_rect  = pygame.Rect(box.x + 6,              strip_y + 5, arrow_size, arrow_size)
    right_arrow_rect = pygame.Rect(box.x + BOX_W - arrow_size - 6, strip_y + 5, arrow_size, arrow_size)
    game_surface.blit(body_font.render("◀", True, GOLD), body_font.render("◀", True, GOLD).get_rect(center=left_arrow_rect.center))
    game_surface.blit(body_font.render("▶", True, GOLD), body_font.render("▶", True, GOLD).get_rect(center=right_arrow_rect.center))

    stock     = stocks[selected_stock_idx]
    content_y = strip_y + strip_h + 14
    left_x    = box.x + 30

    price_color = GREEN if (stock.candles and stock.price >= stock.candles[-1].close) else (RED if stock.candles else BLUE)
    price_surf  = hud_font.render(f"${stock.price:.2f}", True, price_color)
    game_surface.blit(price_surf, (left_x, content_y))
    game_surface.blit(hud_font.render(stock.name, True, WHITE), (left_x + price_surf.get_width() + 16, content_y))

    if len(stock.history) >= 2:
        change  = stock.price - stock.history[-2]
        pct     = (change / stock.history[-2]) * 100 if stock.history[-2] != 0 else 0
        chg_str = f"{'▲' if change >= 0 else '▼'} {abs(change):.2f} ({abs(pct):.2f}%)"
        game_surface.blit(small_font.render(chg_str, True, GREEN if change >= 0 else RED), (left_x, content_y + 28))
    game_surface.blit(small_font.render(f"Candles: {len(stock.candles)}", True, GRAY), (left_x + 250, content_y + 28))

    chart_x, chart_y = left_x, content_y + 55
    chart_w, chart_h = BOX_W - 120, 220
    chart_pad        = 12
    light_green = CANDLE_COLORS["bullish"]["body"];  dark_green = CANDLE_COLORS["bullish"]["border"]
    light_red   = CANDLE_COLORS["bearish"]["body"];  dark_red   = CANDLE_COLORS["bearish"]["border"]
    lgray       = (55, 55, 75)

    chart_rect = pygame.Rect(chart_x, chart_y, chart_w, chart_h)
    pygame.draw.rect(game_surface, (20, 22, 42), chart_rect, border_radius=6)
    pygame.draw.rect(game_surface, (50, 55, 80), chart_rect, 1, border_radius=6)

    if stock.candles:
        candle_w, candle_sp = 8, 3
        total_cw  = candle_w + candle_sp
        max_vis   = (chart_w - 2 * chart_pad - 50) // total_cw
        visible   = stock.candles[-max_vis:]
        min_p, max_p = min(c.low for c in visible), max(c.high for c in visible)
        p_range   = max_p - min_p or 1
        avail_h   = chart_h - 2 * chart_pad
        h_scale   = avail_h / p_range

        def py(price):
            return chart_y + chart_pad + (max_p - price) * h_scale

        for gi in range(6):
            gy = chart_y + chart_pad + (avail_h * gi // 5)
            pygame.draw.line(game_surface, lgray, (chart_x + chart_pad, gy), (chart_x + chart_w - 50, gy), 1)
            game_surface.blit(small_font.render(f"${max_p - (p_range * gi / 5):.1f}", True, GRAY), (chart_x + chart_w - 48, gy - 6))

        cx = chart_x + chart_pad + 4
        for candle in visible:
            body_col = light_green if candle.close >= candle.open else light_red
            bord_col = dark_green  if candle.close >= candle.open else dark_red
            body_top = min(py(candle.open), py(candle.close))
            body_h   = max(1, abs(py(candle.close) - py(candle.open)))
            wick_x   = cx + candle_w // 2
            pygame.draw.line(game_surface, bord_col, (wick_x, int(py(candle.high))), (wick_x, int(py(candle.low))), 1)
            br = pygame.Rect(cx, int(body_top), candle_w, int(body_h))
            pygame.draw.rect(game_surface, body_col, br)
            pygame.draw.rect(game_surface, bord_col, br, 1)
            cx += total_cw
    else:
        no_data = small_font.render("Waiting for market data...", True, GRAY)
        game_surface.blit(no_data, no_data.get_rect(center=chart_rect.center))

    pattern_y = chart_y + chart_h + 14
    if stock.current_pattern_name:
        pinfo  = get_pattern_info(stock.current_pattern_name)
        pcolor = get_pattern_color(stock.current_pattern_name) or GOLD
        if pinfo:
            display_name, category, _ = pinfo
            badge_rect = pygame.Rect(left_x, pattern_y, 260, 28)
            pygame.draw.rect(game_surface, pcolor, badge_rect, border_radius=4)
            game_surface.blit(small_font.render(f"  {display_name}", True, WHITE), (badge_rect.x + 4, badge_rect.y + 4))
            game_surface.blit(small_font.render(category, True, GRAY), (left_x + 270, pattern_y + 4))
            bar_x, bar_w, bar_h, bar_y_pos = left_x + 500, 200, 14, pattern_y + 6
            pygame.draw.rect(game_surface, PATTERN_PROGRESS_BG, (bar_x, bar_y_pos, bar_w, bar_h), border_radius=3)
            pygame.draw.rect(game_surface, (80, 80, 100),       (bar_x, bar_y_pos, bar_w, bar_h), 1, border_radius=3)
            total_ticks = getattr(stock, '_pattern_total_ticks', 20)
            remaining   = (stock._active_segment[0] if stock._active_segment else 0) + sum(s[0] for s in stock._pattern_queue)
            progress    = max(0, total_ticks - remaining) / total_ticks if total_ticks > 0 else 0
            fill_w      = int(bar_w * progress)
            if fill_w > 0:
                pygame.draw.rect(game_surface, pcolor, (bar_x, bar_y_pos, fill_w, bar_h), border_radius=3)
            game_surface.blit(small_font.render(f"{int(progress * 100)}%", True, WHITE), (bar_x + bar_w + 8, bar_y_pos))
    else:
        game_surface.blit(small_font.render("No active pattern — market is drifting", True, GRAY), (left_x, pattern_y + 4))

    # ----------------------------------------------------------------
    # Trading panel (buy/short)
    # ----------------------------------------------------------------
    trade_y = pattern_y + 55 

    owned_qty = player_portfolio.get(stock.name, 0) if player_portfolio else 0
    short_info = player_shorts.get(stock.name) if player_shorts else None
    short_qty = short_info["qty"] if short_info else 0

    portfolio_text = f"Owned: {owned_qty} shares"
    portfolio_surf = small_font.render(portfolio_text, True, (180, 180, 200))
    game_surface.blit(portfolio_surf, (left_x, trade_y))

    # Show short position info next to owned shares
    if short_qty > 0:
        entry_price = short_info["entry_price"]
        pnl = (entry_price - stock.price) * short_qty
        pnl_color = GREEN if pnl >= 0 else RED
        short_text = f"Short: {short_qty} @ ${entry_price:.2f}  P/L: ${pnl:+,.0f}"
        short_surf = small_font.render(short_text, True, pnl_color)
        game_surface.blit(short_surf, (left_x, trade_y + 18))

    cash_text = f"Cash: ${player_cash:,.0f}"
    cash_surf = small_font.render(cash_text, True, GOLD)
    game_surface.blit(cash_surf, (left_x + 220, trade_y)) 

    # --- NEW: Much larger input box ---
    input_x = left_x + 480
    input_y = pattern_y + 44 
    input_w, input_h = 180, 42 
    amount_input_rect = pygame.Rect(input_x, input_y, input_w, input_h)
    
    try:
        from features.interaction import draw_text_input
        draw_text_input(game_surface, amount_input_rect, amount_text, small_font, small_font, input_active)
    except:
        pygame.draw.rect(game_surface, (30, 35, 50), amount_input_rect, border_radius=6)
        if input_active: pygame.draw.rect(game_surface, GOLD, amount_input_rect, 2, border_radius=6)
        else: pygame.draw.rect(game_surface, (60, 70, 90), amount_input_rect, 1, border_radius=6)
        
        display_txt = amount_text if amount_text else "Enter amount..."
        txt_color = WHITE if amount_text else GRAY
        txt_surf = small_font.render(display_txt, True, txt_color)
        game_surface.blit(txt_surf, (amount_input_rect.x + 12, amount_input_rect.y + 10))

    # Buy/Short buttons aligned
    btn_w, btn_h = 90, 36
    btn_y = input_y + (input_h - btn_h) // 2  

    buy_btn = pygame.Rect(input_x + input_w + 15, btn_y, btn_w, btn_h)
    buy_color = (30, 140, 80)  
    if player_cash < stock.price or not amount_text:
        buy_color = (60, 80, 60)  
    draw_button(game_surface, buy_btn, "BUY", small_font, color=buy_color, radius=6)

    short_btn = pygame.Rect(buy_btn.right + 10, btn_y, btn_w, btn_h)
    short_color = (180, 60, 60)  
    if not amount_text:
        short_color = (80, 60, 60)  
    draw_button(game_surface, short_btn, "SHORT", small_font, color=short_color, radius=6)

    # ----------------------------------------------------------------
    # Stock ticker strip at the bottom
    # ----------------------------------------------------------------
    ticker_y = box.y + BOX_H - 36
    pygame.draw.line(game_surface, (40, 44, 65), (box.x + 10, ticker_y - 4), (box.x + BOX_W - 10, ticker_y - 4), 1)
    
    ticker_clip = pygame.Rect(box.x + 10, ticker_y - 5, BOX_W - 20, 40)
    game_surface.set_clip(ticker_clip)

    # Start drawing at the animated offset!
    tx = box.x + 20 + ticker_offset
    
    # Draw the list of stocks TWICE so that it wraps around seamlessly
    for loop in range(2): 
        for s in stocks:
            col   = GREEN if (s.candles and s.price >= s.candles[-1].close) else RED if s.candles else GRAY
            label = small_font.render(f"{s.name} ${s.price:.2f}", True, col)
            game_surface.blit(label, (tx, ticker_y))
            tx += label.get_width() + 30

    game_surface.set_clip(None)

    return left_arrow_rect, right_arrow_rect, buy_btn, short_btn, amount_input_rect, close_btn


def draw_shop_overlay(game_surface, body_font, small_font, player, icon_coin, thumbnails, owned_items, equipped_items, shop_tab, scroll_y):
    from .constants import BLUE, GOLD, GREEN, GRAY, PANEL, WHITE, SHOP_ITEMS
    win_w, win_h = 700, 500
    win_x = (game_surface.get_width()  - win_w) // 2
    win_y = (game_surface.get_height() - win_h) // 2
    box   = pygame.Rect(win_x, win_y, win_w, win_h)
    pygame.draw.rect(game_surface, (40, 45, 60), box, border_radius=8)
    pygame.draw.rect(game_surface, PANEL, box.inflate(-10, -50), border_radius=4)
    game_surface.blit(body_font.render("Shop", True, WHITE), (box.x + 20, box.y + 10))
    close_btn   = draw_close_button(game_surface, box.right - 50, box.y + 10, small_font)
    categories  = ["Desks", "Walls", "Plants", "Upgrades"]
    tab_buttons = []
    tab_x       = box.x + 150
    for cat in categories:
        tab_rect  = pygame.Rect(tab_x, box.y + 15, 100, 30)
        is_active = (cat == shop_tab)
        pygame.draw.rect(game_surface, (60, 80, 160) if is_active else (50, 55, 75), tab_rect, border_radius=4)
        if is_active:
            pygame.draw.rect(game_surface, GOLD, tab_rect, 1, border_radius=4)
        cat_surf = small_font.render(cat, True, WHITE if is_active else GRAY)
        game_surface.blit(cat_surf, cat_surf.get_rect(center=tab_rect.center))
        tab_buttons.append({"rect": tab_rect, "category": cat})
        tab_x += 110

    filtered_items = [item for item in SHOP_ITEMS if item.get("category", "Desks") == shop_tab]
    list_rect      = pygame.Rect(box.x + 10, box.y + 60, win_w - 20, win_h - 70)
    max_scroll     = min(0, list_rect.height - len(filtered_items) * 85 - 20)
    scroll_y       = max(max_scroll, min(0, scroll_y))

    game_surface.set_clip(list_rect)
    buy_buttons = []
    row_y       = list_rect.y + 10 + scroll_y
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
            
            is_placeable = item.get("placeable", False)
            owned_count = owned_items.count(item["id"]) # Count how many we have!
            
            if is_placeable:
                qty_text = small_font.render(f"Owned: {owned_count}", True, GRAY if owned_count == 0 else WHITE)
                game_surface.blit(qty_text, (row_rect.x + 280, row_rect.y + 25))
                
                can_afford = player.cash >= item["price"]
                buy_rect = pygame.Rect(row_rect.right - 90, row_rect.y + 15, 70, 40)
                draw_button(game_surface, buy_rect, "Buy", small_font, color=GREEN if can_afford else (140, 40, 40))
                buy_buttons.append((buy_rect, item, "Buy"))
                
                if owned_count > 0:
                    place_rect = pygame.Rect(row_rect.right - 170, row_rect.y + 15, 70, 40)
                    draw_button(game_surface, place_rect, "Place", small_font, color=BLUE)
                    buy_buttons.append((place_rect, item, "Place"))
                    
            else:
                is_equipped = item["id"] == equipped_items.get(shop_tab)
                btn_rect = pygame.Rect(row_rect.right - 140, row_rect.y + 15, 120, 40)
                
                if is_equipped: btn_text, btn_color = "Equipped", GRAY
                elif owned_count > 0: btn_text, btn_color = "Equip", BLUE
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
    overlay = pygame.Surface((game_surface.get_width(), game_surface.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    game_surface.blit(overlay, (0, 0))
    box_w, box_h = 400, 200
    box_x = (game_surface.get_width()  - box_w) // 2
    box_y = (game_surface.get_height() - box_h) // 2
    box   = pygame.Rect(box_x, box_y, box_w, box_h)
    pygame.draw.rect(game_surface, (40, 45, 60),    box, border_radius=8)
    pygame.draw.rect(game_surface, (200, 200, 220), box, 2, border_radius=8)
    text_surf = body_font.render(prompt_text, True, (255, 255, 255))
    game_surface.blit(text_surf, text_surf.get_rect(centerx=box.centerx, y=box.y + 40))
    yes_btn = pygame.Rect(box_x + 50,  box_y + 120, 120, 50)
    no_btn  = pygame.Rect(box_x + 230, box_y + 120, 120, 50)
    draw_button(game_surface, yes_btn, "Yes", small_font, color=(30, 140, 80))
    draw_button(game_surface, no_btn,  "No",  small_font, color=(140, 40, 40))
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
    
    # --- NEW: Draw the Close Button ---
    close_btn = draw_close_button(game_surface, win_x + win_w - 60, win_y + 10, small_font)
    
    # Split into 2 sections
    left_w = 520
    right_w = win_w - left_w - 60
    section_h = win_h - 90
    
    # Employee Shop
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
            
            # --- INCREASED HEIGHT: Made card taller (125px instead of 90px) ---
            active_card = pygame.Rect(right_x + 15, active_y, right_w - 30, 125)
            
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
            energy_y = active_card.y + 35
            energy_label = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16).render("Energy:", True, LGRAY)
            game_surface.blit(energy_label, (active_card.x + 70, energy_y))
            
            bar_x = active_card.x + 140
            bar_w, bar_h = 160, 16
            pygame.draw.rect(game_surface, (20, 24, 32), (bar_x, energy_y, bar_w, bar_h), border_radius=4)
            pygame.draw.rect(game_surface, (60, 65, 75), (bar_x, energy_y, bar_w, bar_h), 1, border_radius=4)
            
            # Energy fill with dynamic color
            fill_pct = max(0, min(1, emp_npc.energy / emp_npc.max_energy))
            if fill_pct > 0:
                bar_color = GREEN if fill_pct > 0.5 else (255, 180, 0) if fill_pct > 0.25 else RED
                fill_w = int(bar_w * fill_pct)
                pygame.draw.rect(game_surface, bar_color, (bar_x, energy_y, fill_w, bar_h), border_radius=4)
            
            # Energy text overlay
            energy_text = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 14).render(
                f"{int(emp_npc.energy)}/{emp_npc.max_energy}", True, WHITE
            )
            game_surface.blit(energy_text, energy_text.get_rect(center=(bar_x + bar_w // 2, energy_y + bar_h // 2)))
            
            # Speed indicator
            speed_y = active_card.y + 55
            speed_icon = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16).render(
                f"🚀 Speed: {emp_config['effectiveness']}x", True, BLUE
            )
            game_surface.blit(speed_icon, (active_card.x + 70, speed_y))
            
            # --- MOVED: Role and Fire buttons are now underneath everything! ---
            btn_y = active_card.y + 80
            
            # Role Button
            role_btn = pygame.Rect(active_card.x + 70, btn_y, 110, 32)
            role_color = (100, 80, 180) if getattr(emp_npc, 'role', 'Salesman') == "Accountant" else (80, 120, 100)
            draw_button(game_surface, role_btn, getattr(emp_npc, 'role', 'Salesman'), 
                       pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16), 
                       color=role_color, radius=6)

            # Fire button
            fire_btn = pygame.Rect(active_card.x + 190, btn_y, 70, 32)
            draw_button(game_surface, fire_btn, "FIRE", 
                       pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16), 
                       color=(180, 40, 50), radius=6)
            
            # Update rects for clicking
            for btn in staff_buttons:
                if btn["id"] == emp_id:
                    btn["fire_rect"] = fire_btn
                    btn["role_rect"] = role_btn 
                    break
            
            # --- INCREASED SPACING: Move down further for the next card ---
            active_y += 135
 
    return staff_buttons, close_btn

def draw_news_screen(game_surface, title_font, body_font, small_font, news_items, scroll_offset=0, game_clock=None):
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
    for x in range(0, GAME_W, 40):
        pygame.draw.line(game_surface, (30, 30, 55), (x, 0), (x, GAME_H))
    for y in range(0, GAME_H, 40):
        pygame.draw.line(game_surface, (30, 30, 55), (0, y), (GAME_W, y))

    pygame.draw.rect(game_surface, PANEL, pygame.Rect(0, 0, GAME_W, 100))
    pygame.draw.line(game_surface, GOLD, (0, 100), (GAME_W, 100), 2)
    heading = title_font.render("MARKET NEWS", True, GOLD)
    game_surface.blit(heading, heading.get_rect(centerx=GAME_W // 2, y=20))

    back_btn = pygame.Rect(40, 25, 160, 50)
    draw_button(game_surface, back_btn, "← Back", body_font, color=(80, 40, 80))

    IMPACT_COLORS = {
        "positive": (30, 160, 80),
        "negative": (180, 45, 45),
        "neutral":  (80, 100, 160),
    }

    card_w  = GAME_W - 160
    card_h  = 110
    card_x  = 80
    start_y = 120
    gap     = 18

    card_rects = []

    for i, item in enumerate(news_items):
        card_y = start_y + i * (card_h + gap) - scroll_offset

        if card_y + card_h < start_y or card_y > GAME_H:
            card_rects.append((None, item))
            continue

        card_rect  = pygame.Rect(card_x, card_y, card_w, card_h)
        impact_col = IMPACT_COLORS.get(item.get("impact", "neutral"), LGRAY)

        pygame.draw.rect(game_surface, (22, 26, 48), card_rect, border_radius=8)
        pygame.draw.rect(game_surface, impact_col, pygame.Rect(card_x, card_y, 6, card_h), border_radius=4)
        pygame.draw.rect(game_surface, (50, 60, 90), card_rect, 1, border_radius=8)

        # Ticker badge
        ticker_text = item.get("ticker", "???")
        badge_surf  = small_font.render(f" {ticker_text} ", True, DARK)
        badge_rect  = badge_surf.get_rect(x=card_x + 20, y=card_y + 14)
        badge_bg    = badge_rect.inflate(8, 4)
        pygame.draw.rect(game_surface, impact_col, badge_bg, border_radius=4)
        game_surface.blit(badge_surf, badge_rect)

        # Headline — truncated to never overflow the card
        headline_x     = badge_bg.right + 16
        headline_max_w = card_rect.right - headline_x - 16
        headline_text  = item.get("headline", "")
        while headline_text and body_font.size(headline_text)[0] > headline_max_w:
            headline_text = headline_text[:-1]
        if headline_text != item.get("headline", ""):
            headline_text = headline_text[:-3] + "..."
        game_surface.blit(body_font.render(headline_text, True, WHITE), (headline_x, card_y + 12))

        # Summary
        summary = item.get("summary", "")
        if len(summary) > 90:
            summary = summary[:87] + "..."
        game_surface.blit(small_font.render(summary, True, LGRAY), (card_x + 20, card_y + 52))

        # Timestamp — live relative time from game_clock
        if game_clock is not None and "game_timestamp" in item:
            ts_str = game_clock.get_relative_time(item["game_timestamp"])
        else:
            ts_str = item.get("timestamp", "")
        ts_surf = small_font.render(ts_str, True, (90, 100, 130))
        game_surface.blit(ts_surf, ts_surf.get_rect(right=card_rect.right - 16,
                                                     bottom=card_rect.bottom - 10))

        # "Read more" hint
        hint_surf = small_font.render("Click to expand ›", True, (70, 90, 140))
        game_surface.blit(hint_surf, hint_surf.get_rect(right=card_rect.right - 16, y=card_y + 52))

        card_rects.append((card_rect, item))

    total_h = len(news_items) * (card_h + gap)
    if total_h > GAME_H - start_y:
        hint = small_font.render("↑ ↓  Scroll for more", True, (70, 80, 110))
        game_surface.blit(hint, hint.get_rect(centerx=GAME_W // 2, y=GAME_H - 28))

    return back_btn, card_rects


def draw_news_detail(game_surface, title_font, body_font, small_font, item, game_clock=None):
    from .constants import GOLD, GREEN, GRAY

    IMPACT_COLORS = {
        "positive": (30, 160, 80),
        "negative": (180, 45, 45),
        "neutral":  (80, 100, 160),
    }
    impact_col = IMPACT_COLORS.get(item.get("impact", "neutral"), LGRAY)

    overlay = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    game_surface.blit(overlay, (0, 0))

    pan_w, pan_h = 860, 620
    pan_x = (GAME_W - pan_w) // 2
    pan_y = (GAME_H - pan_h) // 2
    panel = pygame.Rect(pan_x, pan_y, pan_w, pan_h)

    pygame.draw.rect(game_surface, (18, 22, 42), panel, border_radius=12)
    pygame.draw.rect(game_surface, impact_col, pygame.Rect(pan_x, pan_y, pan_w, 6), border_radius=12)
    pygame.draw.rect(game_surface, (55, 65, 100), panel, 2, border_radius=12)

    badge_surf = body_font.render(f" {item.get('ticker', '???')} ", True, (10, 10, 20))
    badge_rect = badge_surf.get_rect(x=pan_x + 30, y=pan_y + 26)
    badge_bg   = badge_rect.inflate(12, 6)
    pygame.draw.rect(game_surface, impact_col, badge_bg, border_radius=5)
    game_surface.blit(badge_surf, badge_rect)
    game_surface.blit(
        small_font.render(item.get("impact", "neutral").upper(), True, impact_col),
        (badge_bg.right + 14, pan_y + 32)
    )

    # Timestamp — live relative time from game_clock
    if game_clock is not None and "game_timestamp" in item:
        ts_str = game_clock.get_relative_time(item["game_timestamp"])
    else:
        ts_str = item.get("timestamp", "")
    ts_surf = small_font.render(ts_str, True, (90, 100, 130))
    game_surface.blit(ts_surf, ts_surf.get_rect(right=panel.right - 24, y=pan_y + 32))

    pygame.draw.line(game_surface, (40, 50, 80), (pan_x + 20, pan_y + 72), (pan_x + pan_w - 20, pan_y + 72), 1)

    y = pan_y + 84
    game_surface.blit(body_font.render(item.get("headline", ""), True, WHITE), (pan_x + 30, y))
    y += body_font.get_linesize() + 8
    game_surface.blit(small_font.render(item.get("summary", ""), True, LGRAY), (pan_x + 30, y))
    y += small_font.get_linesize() + 12
    pygame.draw.line(game_surface, (40, 50, 80), (pan_x + 20, y), (pan_x + pan_w - 20, y), 1)
    y += 12

    max_width = pan_w - 60
    words     = item.get("body", "No further details available.").split()
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

    close_btn = pygame.Rect(panel.right - 150, panel.bottom - 60, 120, 40)
    draw_button(game_surface, close_btn, "✕  Close", small_font, color=(120, 40, 40))
    return close_btn


def draw_close_button(game_surface, x, y, font):
    btn_rect = pygame.Rect(x, y, 40, 40)
    pygame.draw.rect(game_surface, (180, 50, 50), btn_rect, border_radius=6)
    pygame.draw.rect(game_surface, (255, 100, 100), btn_rect, 2, border_radius=6)
    x_text = font.render("X", True, (255, 255, 255))
    game_surface.blit(x_text, x_text.get_rect(center=btn_rect.center))
    
    return btn_rect

def draw_sleep_bubble(game_surface, x, y, font):
    """Draws a speech bubble for resting employees."""

    white = (255, 255, 255)
    dark_blue = (25, 30, 60)       
    shadow_color = (180, 190, 220) 

    bubble_w = 48
    bubble_h = 32

    tail_pts = [(x + 12, y + bubble_h - 2),  
                (x + 22, y + bubble_h - 2),  
                (x + 12, y + bubble_h + 8)]  
    
    pygame.draw.polygon(game_surface, shadow_color, tail_pts)
    pygame.draw.polygon(game_surface, dark_blue, tail_pts, 2) 
    full_rect = pygame.Rect(x, y, bubble_w, bubble_h)
    pygame.draw.rect(game_surface, shadow_color, full_rect, border_radius=6)

    white_rect = pygame.Rect(x, y, bubble_w, bubble_h - 4)
    pygame.draw.rect(game_surface, white, white_rect, border_radius=6)

    #  Draw the main outer border
    pygame.draw.rect(game_surface, dark_blue, full_rect, width=2, border_radius=6)

    pygame.draw.line(game_surface, shadow_color, (x + 14, y + bubble_h - 2), (x + 20, y + bubble_h - 2), 2)

    z1 = font.render("Z", True, dark_blue)
    z2 = font.render("z", True, dark_blue)
    z3 = font.render("z", True, dark_blue)


    game_surface.blit(z1, (x + 14, y))
    game_surface.blit(z2, (x + 26, y + 7))
    game_surface.blit(z3, (x + 16, y + 10))
def draw_accounts_screen(game_surface, title_font, body_font, small_font, player):
    """Draws a banking/accounts screen to manage offshore and tax data."""
    from .constants import GOLD, WHITE, GRAY, GREEN, RED
    
    win_w, win_h = 700, 450
    win_x, win_y = (game_surface.get_width() - win_w) // 2, (game_surface.get_height() - win_h) // 2
    box = pygame.Rect(win_x, win_y, win_w, win_h)
    
    pygame.draw.rect(game_surface, (20, 24, 32), box, border_radius=12)
    pygame.draw.rect(game_surface, (50, 60, 80), box, 3, border_radius=12)
    
    title = body_font.render("🏦 Financial Accounts", True, GOLD)
    game_surface.blit(title, (box.x + 30, box.y + 20))
    
    close_btn = pygame.Rect(box.right - 50, box.y + 15, 35, 35)
    pygame.draw.rect(game_surface, (180, 50, 50), close_btn, border_radius=6)
    x_text = small_font.render("X", True, WHITE)
    game_surface.blit(x_text, x_text.get_rect(center=close_btn.center))

    # Main Cash
    cash_rect = pygame.Rect(box.x + 40, box.y + 100, win_w - 80, 80)
    pygame.draw.rect(game_surface, (30, 35, 45), cash_rect, border_radius=8)
    game_surface.blit(small_font.render("Liquid Cash (Taxable)", True, GRAY), (cash_rect.x + 20, cash_rect.y + 15))
    game_surface.blit(small_font.render(f"${player.cash:,.2f}", True, GREEN), (cash_rect.x + 20, cash_rect.y + 45))

    # Offshore Account
    off_rect = pygame.Rect(box.x + 40, box.y + 200, win_w - 80, 80)
    pygame.draw.rect(game_surface, (30, 35, 45), off_rect, border_radius=8)
    game_surface.blit(small_font.render("Offshore Account (Untouchable)", True, GRAY), (off_rect.x + 20, off_rect.y + 15))
    game_surface.blit(small_font.render(f"${player.offshore:,.2f}", True, (0, 200, 255)), (off_rect.x + 20, off_rect.y + 45))

    # Repatriate Button
    repat_btn = pygame.Rect(off_rect.right - 220, off_rect.y + 20, 200, 40)
    pygame.draw.rect(game_surface, (40, 100, 160) if player.offshore > 0 else (60, 60, 70), repat_btn, border_radius=6)
    r_text_font = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16)
    r_text = r_text_font.render("Repatriate (10% Tax)", True, WHITE if player.offshore > 0 else GRAY)
    game_surface.blit(r_text, r_text.get_rect(center=repat_btn.center))

    # Tax Liability
    tax_rect = pygame.Rect(box.x + 40, box.y + 300, win_w - 80, 80)
    pygame.draw.rect(game_surface, (45, 25, 25), tax_rect, border_radius=8)
    pygame.draw.rect(game_surface, RED, tax_rect, 1, border_radius=8)
    game_surface.blit(small_font.render("Pending Tax Liability", True, (255, 150, 150)), (tax_rect.x + 20, tax_rect.y + 15))
    game_surface.blit(small_font.render(f"${player.owed_taxes:,.2f}", True, RED), (tax_rect.x + 20, tax_rect.y + 45))

    return close_btn, repat_btn

def draw_interaction_prompt(surface, font, text, center_x, bottom_y, border_color=(80, 200, 120)):
    """Draws a dynamic, centered interaction prompt box."""
    import pygame
    
    # Render text first to get its exact dimensions
    text_surf = font.render(text, True, (255, 255, 255))
    text_w, text_h = text_surf.get_size()
    
    # Calculate box dimensions with padding
    padding_x = 15
    padding_y = 6
    box_w = text_w + (padding_x * 2)
    box_h = text_h + (padding_y * 2)
    
    # Position the box (centered horizontally, anchored at the bottom)
    box_x = center_x - (box_w // 2)
    box_y = bottom_y - box_h
    box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
    
    # Draw dark background and dynamic border
    pygame.draw.rect(surface, (30, 34, 45), box_rect, border_radius=6)
    pygame.draw.rect(surface, border_color, box_rect, 2, border_radius=6)
    
    # Draw text exactly in the center of the box
    surface.blit(text_surf, (box_x + padding_x, box_y + padding_y))

def draw_day_night_cycle(game_surface, game_clock, player, computer_rect):
    """Draws a dynamic day/night lighting cycle over the office."""
    import pygame
    
    # Calculate time as a smooth float (e.g., 18.5 is 6:30 PM)
    time_val = game_clock.current_time.hour + (game_clock.current_time.minute / 60.0)

    # 1. Calculate Darkness Level (1.0 is bright noon, 0.35 is pitch black night)
    min_light = 0.35
    if 8.0 <= time_val <= 16.0:
        intensity = 1.0   # Day
    elif 16.0 < time_val < 19.0:
        intensity = min_light + (1.0 - min_light) * (1.0 - ((time_val - 16.0) / 3.0)) # Sunset fade
    elif 19.0 <= time_val <= 24.0 or 0.0 <= time_val <= 5.0:
        intensity = min_light # Deep Night
    elif 5.0 < time_val < 8.0:
        intensity = min_light + (1.0 - min_light) * ((time_val - 5.0) / 3.0) # Sunrise fade

    if intensity >= 0.99:
        return # Skip drawing if it's full daylight

    # 2. Create the Lighting Canvas
    r = int(255 * intensity)
    g = int(255 * intensity)
    b = int(255 * max(intensity, 0.55)) 
    
    overlay = pygame.Surface(game_surface.get_size())
    overlay.fill((r, g, b))

    # 3. Add Soft Glowing Lights (Using Additive Blending)
    if intensity < 0.8:
        glow_max = int(255 * (1.0 - intensity) * 0.9) 

        def draw_light(center, radius, color_rgb):
            light_surf = pygame.Surface((radius * 2, radius * 2))
            light_surf.fill((0, 0, 0)) 
            for i in range(10, 0, -1):
                pct = i / 10.0
                c = (int(color_rgb[0] * pct), int(color_rgb[1] * pct), int(color_rgb[2] * pct))
                pygame.draw.circle(light_surf, c, (radius, radius), int(radius * (1.0 - pct)))
            overlay.blit(light_surf, (center[0] - radius, center[1] - radius), special_flags=pygame.BLEND_RGB_ADD)

        # Draw a warm aura around the Player
        draw_light((player.x +44, player.y + 40), 160, (glow_max, glow_max, int(glow_max*0.8)))
        
        # Draw a bright cyan glow emitting from the computer monitors
        if computer_rect:
            draw_light(computer_rect.center, 140, (int(glow_max*0.5), int(glow_max*0.9), glow_max)) 

    # 4. Multiply the lighting canvas onto the main screen
    game_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_MULT)