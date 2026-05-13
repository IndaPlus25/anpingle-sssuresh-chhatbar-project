import pygame
from .constants import GAME_W, GAME_H, DARK, GOLD, LGRAY, PANEL, WHITE, CHARACTERS
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

def draw_market_overlay(game_surface, body_font, hud_font, small_font, stocks,
                         selected_stock_idx=0):
    """Draws the Stock Market interaction menu with candlestick charts and pattern info.

    Returns (left_arrow_rect, right_arrow_rect) for click-based stock navigation.
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

    return left_arrow_rect, right_arrow_rect

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

def draw_close_button(game_surface, x, y, font):
    """Draws a red rectangular close button with an X."""
    btn_rect = pygame.Rect(x, y, 40, 40)
    pygame.draw.rect(game_surface, (180, 50, 50), btn_rect, border_radius=6)
    pygame.draw.rect(game_surface, (255, 100, 100), btn_rect, 2, border_radius=6)
    
    x_text = font.render("X", True, (255, 255, 255))
    # Push the X slightly up/down depending on your font so it centers perfectly
    game_surface.blit(x_text, x_text.get_rect(center=btn_rect.center))
    
    return btn_rect