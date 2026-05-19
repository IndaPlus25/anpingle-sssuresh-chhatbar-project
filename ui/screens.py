import pygame
from .constants import GAME_W, GAME_H, DARK, GOLD, LGRAY, PANEL, WHITE, RED, GREEN, BLUE, GRAY, CHARACTERS
from features.interaction import draw_button

def draw_menu(game_surface, title_font, body_font, small_font, icon_play, icon_person, icon_quit, icon_settings=None):
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
    settings_btn = pygame.Rect(490, 520, 300, 60)
    quit_btn  = pygame.Rect(490, 440, 300, 60)
    draw_button(game_surface, start_btn, "START  (Enter)", small_font, color=(30, 140, 80), icon=icon_play)
    draw_button(game_surface, char_btn,  "Characters",     small_font, color=(60, 80, 160), icon=icon_person)
    draw_button(game_surface, settings_btn, "Settings", small_font, color=(90, 75, 35), icon=icon_settings)
    draw_button(game_surface, quit_btn,  "Quit  (Q)",      small_font, color=(140, 40, 40), icon=icon_quit)
    return start_btn, char_btn, settings_btn, quit_btn


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
            img_rect = img.get_rect(centerx=rect.centerx, y=180)
            game_surface.blit(img, img_rect)
        game_surface.blit(body_font.render(char["name"], True, WHITE if i == selected_idx else LGRAY),
                          body_font.render(char["name"], True, WHITE).get_rect(centerx=rect.centerx, y=330))
        game_surface.blit(small_font.render(char["desc"], True, LGRAY),
                          small_font.render(char["desc"], True, LGRAY).get_rect(centerx=rect.centerx, y=360))
    back_btn    = pygame.Rect(60,   620, 180, 50)
    confirm_btn = pygame.Rect(1040, 620, 180, 50)
    # STRIPPED ARROWS/CHECKMARKS
    draw_button(game_surface, back_btn,    "< Back",    body_font, color=(80, 40, 80))
    draw_button(game_surface, confirm_btn, "Confirm", body_font, color=(30, 140, 80))
    return card_rects, back_btn, confirm_btn


def draw_text_input(game_surface, rect, text, font, placeholder_font, is_active=False, placeholder="Enter amount..."):
    bg_color = (30, 35, 55) if is_active else (20, 22, 42)
    border_color = GOLD if is_active else (60, 70, 90)
    pygame.draw.rect(game_surface, bg_color, rect, border_radius=6)
    pygame.draw.rect(game_surface, border_color, rect, 2, border_radius=6)

    if text:
        text_surf = font.render(text, True, WHITE)
    else:
        text_surf = placeholder_font.render(placeholder, True, (100, 100, 120))

    text_rect = text_surf.get_rect(midleft=(rect.x + 12, rect.centery))
    game_surface.blit(text_surf, text_rect)

    if is_active:
        cursor_x = text_rect.right + 2
        cursor_y = rect.y + 8
        cursor_height = rect.height - 16
        pygame.draw.line(game_surface, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

    return rect


def draw_market_overlay(game_surface, body_font, hud_font, small_font, stocks,
                         selected_stock_idx=0, player_cash=0, player_portfolio=None,
                         amount_text="", input_active=False, ticker_offset=0):
    from .constants import BLUE, GOLD, GREEN, GRAY, RED, WHITE, DARK
    from .assets.stock_assets import CANDLE_COLORS, PATTERN_PROGRESS_BG, get_pattern_color, get_pattern_info

    BOX_W, BOX_H = 1020, 600 
    box_x = (game_surface.get_width()  - BOX_W) // 2
    box_y = (game_surface.get_height() - BOX_H) // 2
    box   = pygame.Rect(box_x, box_y, BOX_W, BOX_H)

    overlay = pygame.Surface((game_surface.get_width(), game_surface.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    game_surface.blit(overlay, (0, 0))

    pygame.draw.rect(game_surface, (10, 12, 28), box, border_radius=14)
    pygame.draw.rect(game_surface, BLUE, box, 2, border_radius=14)

    game_surface.blit(body_font.render("[ STOCK MARKET ]", True, GOLD), (box.x + 30, box.y + 16))
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
    
    # REPLACED UNICODE ARROWS WITH PLAIN TEXT < >
    game_surface.blit(body_font.render("<", True, GOLD), body_font.render("<", True, GOLD).get_rect(center=left_arrow_rect.center))
    game_surface.blit(body_font.render(">", True, GOLD), body_font.render(">", True, GOLD).get_rect(center=right_arrow_rect.center))

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
        # REPLACED UNICODE ARROWS WITH +/-
        chg_str = f"{'+' if change >= 0 else '-'} {abs(change):.2f} ({abs(pct):.2f}%)"
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

    trade_y = pattern_y + 55 
    owned_qty = player_portfolio.get(stock.name, 0) if player_portfolio else 0

    portfolio_text = f"Owned: {owned_qty} shares"
    portfolio_surf = small_font.render(portfolio_text, True, (180, 180, 200))
    game_surface.blit(portfolio_surf, (left_x, trade_y))

    cash_text = f"Cash: ${player_cash:,.0f}"
    cash_surf = small_font.render(cash_text, True, GOLD)
    game_surface.blit(cash_surf, (left_x + 220, trade_y)) 

    input_x = left_x + 480
    input_y = pattern_y + 44 
    input_w, input_h = 180, 42 
    amount_input_rect = pygame.Rect(input_x, input_y, input_w, input_h)
    
    try:
        from features.interaction import draw_text_input as external_draw_text_input
        external_draw_text_input(game_surface, amount_input_rect, amount_text, small_font, small_font, input_active)
    except:
        pygame.draw.rect(game_surface, (30, 35, 50), amount_input_rect, border_radius=6)
        if input_active: pygame.draw.rect(game_surface, GOLD, amount_input_rect, 2, border_radius=6)
        else: pygame.draw.rect(game_surface, (60, 70, 90), amount_input_rect, 1, border_radius=6)
        
        display_txt = amount_text if amount_text else "Enter amount..."
        txt_color = WHITE if amount_text else GRAY
        txt_surf = small_font.render(display_txt, True, txt_color)
        game_surface.blit(txt_surf, (amount_input_rect.x + 12, amount_input_rect.y + 10))

    btn_w, btn_h = 90, 36
    btn_y = input_y + (input_h - btn_h) // 2  

    buy_btn = pygame.Rect(input_x + input_w + 15, btn_y, btn_w, btn_h)
    buy_color = (30, 140, 80)  
    if player_cash < stock.price or not amount_text:
        buy_color = (60, 80, 60)  
    draw_button(game_surface, buy_btn, "BUY", small_font, color=buy_color, radius=6)

    sell_btn = pygame.Rect(buy_btn.right + 10, btn_y, btn_w, btn_h)
    sell_color = (180, 60, 60)  
    if owned_qty <= 0 or not amount_text:
        sell_color = (80, 60, 60)  
    draw_button(game_surface, sell_btn, "SELL", small_font, color=sell_color, radius=6)

    ticker_y = box.y + BOX_H - 36
    pygame.draw.line(game_surface, (40, 44, 65), (box.x + 10, ticker_y - 4), (box.x + BOX_W - 10, ticker_y - 4), 1)
    
    ticker_clip = pygame.Rect(box.x + 10, ticker_y - 5, BOX_W - 20, 40)
    game_surface.set_clip(ticker_clip)

    tx = box.x + 20 + ticker_offset
    for loop in range(2): 
        for s in stocks:
            col   = GREEN if (s.candles and s.price >= s.candles[-1].close) else RED if s.candles else GRAY
            label = small_font.render(f"{s.name} ${s.price:.2f}", True, col)
            game_surface.blit(label, (tx, ticker_y))
            tx += label.get_width() + 30

    game_surface.set_clip(None)
    return left_arrow_rect, right_arrow_rect, buy_btn, sell_btn, amount_input_rect, close_btn


def draw_shop_overlay(game_surface, body_font, small_font, player, icon_coin, thumbnails, owned_items, equipped_items, shop_tab, scroll_y):
    from .constants import BLUE, GOLD, GREEN, GRAY, PANEL, WHITE, SHOP_ITEMS
    win_w, win_h = 700, 500
    win_x = (game_surface.get_width()  - win_w) // 2
    win_y = (game_surface.get_height() - win_h) // 2
    box   = pygame.Rect(win_x, win_y, win_w, win_h)
    pygame.draw.rect(game_surface, (40, 45, 60), box, border_radius=8)
    pygame.draw.rect(game_surface, PANEL, box.inflate(-10, -50), border_radius=4)
    game_surface.blit(body_font.render("[ SHOP ]", True, GOLD), (box.x + 20, box.y + 10))
    close_btn   = draw_close_button(game_surface, box.right - 50, box.y + 10, small_font)
    categories  = ["Desks", "Walls", "Plants", "Upgrades"]
    tab_buttons = []
    tab_x       = box.x + 170
    for cat in categories:
        tab_rect  = pygame.Rect(tab_x, box.y + 20, 100, 30)
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
            owned_count = owned_items.count(item["id"])
            
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
    from .constants import BLUE, GOLD, GREEN, GRAY, RED, PANEL, WHITE
    
    win_w, win_h = 1100, 600
    win_x, win_y = (game_surface.get_width() - win_w) // 2, (game_surface.get_height() - win_h) // 2
    main_box = pygame.Rect(win_x, win_y, win_w, win_h)
    
    pygame.draw.rect(game_surface, (25, 28, 38), main_box, border_radius=12)
    pygame.draw.rect(game_surface, (60, 70, 90), main_box, 3, border_radius=12)
    
    header_rect = pygame.Rect(win_x, win_y, win_w, 60)
    pygame.draw.rect(game_surface, (35, 40, 55), header_rect, border_top_left_radius=12, border_top_right_radius=12)
    pygame.draw.line(game_surface, (80, 90, 110), (win_x, win_y + 60), (win_x + win_w, win_y + 60), 2)
    
    title = body_font.render("[ STAFF MANAGEMENT ]", True, GOLD)
    game_surface.blit(title, (win_x + 30, win_y + 15))
    
    close_btn = draw_close_button(game_surface, win_x + win_w - 60, win_y + 10, small_font)
    
    left_w = 520
    right_w = win_w - left_w - 60
    section_h = win_h - 90
    
    left_x = win_x + 20
    left_y = win_y + 75
    left_box = pygame.Rect(left_x, left_y, left_w, section_h)
    
    pygame.draw.rect(game_surface, (30, 34, 45), left_box, border_radius=8)
    pygame.draw.rect(game_surface, (50, 60, 75), left_box, 2, border_radius=8)
    
    shop_title = small_font.render("> AVAILABLE FOR HIRE", True, WHITE)
    game_surface.blit(shop_title, (left_x + 15, left_y + 10))
    pygame.draw.line(game_surface, (60, 70, 85), (left_x + 10, left_y + 45), (left_x + left_w - 10, left_y + 45), 1)
    
    right_x = left_x + left_w + 20
    right_y = left_y
    right_box = pygame.Rect(right_x, right_y, right_w, section_h)
    
    pygame.draw.rect(game_surface, (30, 34, 45), right_box, border_radius=8)
    pygame.draw.rect(game_surface, (50, 60, 75), right_box, 2, border_radius=8)
    
    active_title = small_font.render("> ACTIVE STAFF", True, WHITE)
    game_surface.blit(active_title, (right_x + 15, right_y + 10))
    
    staff_count = len(active_staff)
    badge_text = small_font.render(f"{staff_count}", True, WHITE)
    badge_rect = pygame.Rect(right_x + right_w - 50, right_y + 8, 35, 30)
    pygame.draw.rect(game_surface, GREEN if staff_count > 0 else GRAY, badge_rect, border_radius=15)
    game_surface.blit(badge_text, badge_text.get_rect(center=badge_rect.center))
    
    pygame.draw.line(game_surface, (60, 70, 85), (right_x + 10, right_y + 45), (right_x + right_w - 10, right_y + 45), 1)
    
    staff_buttons = []
    shop_y = left_y + 60
    
    stat_font = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 18)
    btn_font = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 20)
    
    for emp in available_employees:
        emp_id = emp["id"]
        is_hired = emp_id in active_staff
        
        card_rect = pygame.Rect(left_x + 15, shop_y, left_w - 30, 110)
        bg_color = (38, 42, 55) if not is_hired else (28, 32, 42)
        pygame.draw.rect(game_surface, bg_color, card_rect, border_radius=8)
        pygame.draw.rect(game_surface, (70, 80, 100) if not is_hired else (50, 55, 65), card_rect, 2, border_radius=8)
        
        port_rect = pygame.Rect(card_rect.x + 12, card_rect.y + 12, 60, 60)
        pygame.draw.rect(game_surface, (20, 24, 32), port_rect, border_radius=6)
        
        port = portraits.get(emp_id)
        if port:
            port_scaled = pygame.transform.scale(port, (56, 56))
            game_surface.blit(port_scaled, (port_rect.x + 2, port_rect.y + 2))
        
        name_surf = small_font.render(emp["name"], True, WHITE if not is_hired else GRAY)
        game_surface.blit(name_surf, (card_rect.x + 85, card_rect.y + 12))
        
        stats_y = card_rect.y + 42
        energy_label = stat_font.render("ENG:", True, GOLD)
        game_surface.blit(energy_label, (card_rect.x + 85, stats_y))
        
        energy_text = stat_font.render(f"{emp['max_energy']}", True, (200, 200, 200))
        game_surface.blit(energy_text, (card_rect.x + 130, stats_y))
        
        speed_label = stat_font.render("SPD:", True, BLUE)
        game_surface.blit(speed_label, (card_rect.x + 180, stats_y))
        
        speed_text = stat_font.render(f"{emp['effectiveness']}x", True, (200, 200, 200))
        game_surface.blit(speed_text, (card_rect.x + 225, stats_y))
        
        salary_rect = pygame.Rect(card_rect.x + 85, card_rect.y + 68, 160, 28)
        pygame.draw.rect(game_surface, (45, 50, 65), salary_rect, border_radius=5)
        
        sal_text = stat_font.render(f"PAY: ${emp['salary']}/hr", True, GOLD)
        game_surface.blit(sal_text, (salary_rect.x + 8, salary_rect.y + 5))
        
        hire_btn = pygame.Rect(card_rect.right - 95, card_rect.y + 35, 80, 40)
        if is_hired:
            btn_color = (60, 60, 70)
            btn_text = "HIRED"
        else:
            btn_color = (40, 150, 80)
            btn_text = "HIRE"
        
        draw_button(game_surface, hire_btn, btn_text, btn_font, color=btn_color, radius=6)
        
        staff_buttons.append({
            "id": emp_id, 
            "hire_rect": hire_btn, 
            "fire_rect": pygame.Rect(0, 0, 0, 0),
            "config": emp
        })
        shop_y += 125

    active_y = right_y + 60
    if len(active_staff) == 0:
        empty_text = small_font.render("No active employees", True, GRAY)
        game_surface.blit(empty_text, empty_text.get_rect(centerx=right_box.centerx, y=active_y + 100))
        hint_text = stat_font.render("Hire staff from the left panel", True, GRAY)
        game_surface.blit(hint_text, hint_text.get_rect(centerx=right_box.centerx, y=active_y + 130))
    else:
        for emp_id, emp_npc in active_staff.items():
            emp_config = emp_npc.config
            active_card = pygame.Rect(right_x + 15, active_y, right_w - 30, 125)
            
            pygame.draw.rect(game_surface, (38, 42, 55), active_card, border_radius=8)
            pygame.draw.rect(game_surface, (60, 140, 80), active_card, 2, border_radius=8)
            
            port_rect_active = pygame.Rect(active_card.x + 10, active_card.y + 10, 50, 50)
            pygame.draw.rect(game_surface, (20, 24, 32), port_rect_active, border_radius=6)
            
            port = portraits.get(emp_id)
            if port:
                port_scaled = pygame.transform.scale(port, (46, 46))
                game_surface.blit(port_scaled, (port_rect_active.x + 2, port_rect_active.y + 2))
            
            name_surf = btn_font.render(emp_config["name"], True, WHITE)
            game_surface.blit(name_surf, (active_card.x + 70, active_card.y + 10))
            
            energy_y = active_card.y + 35
            energy_label = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16).render("Energy:", True, LGRAY)
            game_surface.blit(energy_label, (active_card.x + 70, energy_y))
            
            bar_x = active_card.x + 140
            bar_w, bar_h = 160, 16
            pygame.draw.rect(game_surface, (20, 24, 32), (bar_x, energy_y, bar_w, bar_h), border_radius=4)
            pygame.draw.rect(game_surface, (60, 65, 75), (bar_x, energy_y, bar_w, bar_h), 1, border_radius=4)
            
            fill_pct = max(0, min(1, emp_npc.energy / emp_npc.max_energy))
            if fill_pct > 0:
                bar_color = GREEN if fill_pct > 0.5 else (255, 180, 0) if fill_pct > 0.25 else RED
                fill_w = int(bar_w * fill_pct)
                pygame.draw.rect(game_surface, bar_color, (bar_x, energy_y, fill_w, bar_h), border_radius=4)
            
            energy_text = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 14).render(
                f"{int(emp_npc.energy)}/{emp_npc.max_energy}", True, WHITE
            )
            game_surface.blit(energy_text, energy_text.get_rect(center=(bar_x + bar_w // 2, energy_y + bar_h // 2)))
            
            speed_y = active_card.y + 55
            speed_icon = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16).render(
                f"SPD: {emp_config['effectiveness']}x", True, BLUE
            )
            game_surface.blit(speed_icon, (active_card.x + 70, speed_y))
            
            btn_y = active_card.y + 80
            role_btn = pygame.Rect(active_card.x + 70, btn_y, 110, 32)
            role_color = (100, 80, 180) if getattr(emp_npc, 'role', 'Salesman') == "Accountant" else (80, 120, 100)
            draw_button(game_surface, role_btn, getattr(emp_npc, 'role', 'Salesman'), 
                       pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16), 
                       color=role_color, radius=6)

            fire_btn = pygame.Rect(active_card.x + 190, btn_y, 70, 32)
            draw_button(game_surface, fire_btn, "FIRE", 
                       pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16), 
                       color=(180, 40, 50), radius=6)
            
            for btn in staff_buttons:
                if btn["id"] == emp_id:
                    btn["fire_rect"] = fire_btn
                    btn["role_rect"] = role_btn 
                    break
            active_y += 135
 
    return staff_buttons, close_btn

def draw_news_screen(game_surface, title_font, body_font, small_font, news_items, scroll_offset=0, game_clock=None):
    from .constants import BLUE, GOLD, GREEN, GRAY, RED
    game_surface.fill(DARK)
    for x in range(0, GAME_W, 40):
        pygame.draw.line(game_surface, (30, 30, 55), (x, 0), (x, GAME_H))
    for y in range(0, GAME_H, 40):
        pygame.draw.line(game_surface, (30, 30, 55), (0, y), (GAME_W, y))

    pygame.draw.rect(game_surface, PANEL, pygame.Rect(0, 0, GAME_W, 100))
    pygame.draw.line(game_surface, GOLD, (0, 100), (GAME_W, 100), 2)
    heading = title_font.render("[ MARKET NEWS ]", True, GOLD)
    game_surface.blit(heading, heading.get_rect(centerx=GAME_W // 2, y=20))

    back_btn = pygame.Rect(40, 25, 160, 50)
    draw_button(game_surface, back_btn, "< Back", body_font, color=(80, 40, 80))

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

        ticker_text = item.get("ticker", "???")
        badge_surf  = small_font.render(f" {ticker_text} ", True, DARK)
        badge_rect  = badge_surf.get_rect(x=card_x + 20, y=card_y + 14)
        badge_bg    = badge_rect.inflate(8, 4)
        pygame.draw.rect(game_surface, impact_col, badge_bg, border_radius=4)
        game_surface.blit(badge_surf, badge_rect)

        headline_x     = badge_bg.right + 16
        headline_max_w = card_rect.right - headline_x - 16
        headline_text  = item.get("headline", "")
        while headline_text and body_font.size(headline_text)[0] > headline_max_w:
            headline_text = headline_text[:-1]
        if headline_text != item.get("headline", ""):
            headline_text = headline_text[:-3] + "..."
        game_surface.blit(body_font.render(headline_text, True, WHITE), (headline_x, card_y + 12))

        summary = item.get("summary", "")
        if len(summary) > 90:
            summary = summary[:87] + "..."
        game_surface.blit(small_font.render(summary, True, LGRAY), (card_x + 20, card_y + 52))

        if game_clock is not None and "game_timestamp" in item:
            ts_str = game_clock.get_relative_time(item["game_timestamp"])
        else:
            ts_str = item.get("timestamp", "")
        ts_surf = small_font.render(ts_str, True, (90, 100, 130))
        game_surface.blit(ts_surf, ts_surf.get_rect(right=card_rect.right - 16, bottom=card_rect.bottom - 10))

        hint_surf = small_font.render("Click to expand >", True, (70, 90, 140))
        game_surface.blit(hint_surf, hint_surf.get_rect(right=card_rect.right - 16, y=card_y + 52))

        card_rects.append((card_rect, item))

    total_h = len(news_items) * (card_h + gap)
    if total_h > GAME_H - start_y:
        hint = small_font.render("Scroll for more", True, (70, 80, 110))
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
    game_surface.blit(small_font.render(item.get("impact", "neutral").upper(), True, impact_col), (badge_bg.right + 14, pan_y + 32))

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
            if current: lines.append(current)
            current = word
    if current: lines.append(current)
    for line in lines:
        if y > pan_y + pan_h - 100: break
        game_surface.blit(small_font.render(line, True, (190, 200, 220)), (pan_x + 30, y))
        y += small_font.get_linesize()

    related = item.get("related", [])
    if related:
        pygame.draw.line(game_surface, (40, 50, 80), (pan_x + 20, pan_y + pan_h - 90), (pan_x + pan_w - 20, pan_y + pan_h - 90), 1)
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
    draw_button(game_surface, close_btn, "X  Close", small_font, color=(120, 40, 40))
    return close_btn


def draw_close_button(game_surface, x, y, font):
    btn_rect = pygame.Rect(x, y, 40, 40)
    pygame.draw.rect(game_surface, (180, 50, 50), btn_rect, border_radius=6)
    pygame.draw.rect(game_surface, (255, 100, 100), btn_rect, 2, border_radius=6)
    x_text = font.render("X", True, (255, 255, 255))
    game_surface.blit(x_text, x_text.get_rect(centerx=btn_rect.centerx, centery=btn_rect.centery - 2))
    return btn_rect


def draw_sleep_bubble(game_surface, x, y, font):
    white = (255, 255, 255)
    dark_blue = (25, 30, 60)       
    shadow_color = (180, 190, 220) 
    bubble_w, bubble_h = 48, 32
    tail_pts = [(x + 12, y + bubble_h - 2), (x + 22, y + bubble_h - 2), (x + 12, y + bubble_h + 8)]  
    
    pygame.draw.polygon(game_surface, shadow_color, tail_pts)
    pygame.draw.polygon(game_surface, dark_blue, tail_pts, 2) 
    full_rect = pygame.Rect(x, y, bubble_w, bubble_h)
    pygame.draw.rect(game_surface, shadow_color, full_rect, border_radius=6)

    white_rect = pygame.Rect(x, y, bubble_w, bubble_h - 4)
    pygame.draw.rect(game_surface, white, white_rect, border_radius=6)
    pygame.draw.rect(game_surface, dark_blue, full_rect, width=2, border_radius=6)
    pygame.draw.line(game_surface, shadow_color, (x + 14, y + bubble_h - 2), (x + 20, y + bubble_h - 2), 2)

    z1 = font.render("Z", True, dark_blue)
    z2 = font.render("z", True, dark_blue)
    z3 = font.render("z", True, dark_blue)
    game_surface.blit(z1, (x + 14, y))
    game_surface.blit(z2, (x + 26, y + 7))
    game_surface.blit(z3, (x + 16, y + 10))


def draw_accounts_screen(game_surface, title_font, body_font, small_font, player):
    from .constants import GOLD, WHITE, GRAY, GREEN, RED
    win_w, win_h = 700, 450
    win_x, win_y = (game_surface.get_width() - win_w) // 2, (game_surface.get_height() - win_h) // 2
    box = pygame.Rect(win_x, win_y, win_w, win_h)
    
    pygame.draw.rect(game_surface, (20, 24, 32), box, border_radius=12)
    pygame.draw.rect(game_surface, (50, 60, 80), box, 3, border_radius=12)
    
    title = body_font.render("[ FINANCIAL ACCOUNTS ]", True, GOLD)
    game_surface.blit(title, (box.x + 30, box.y + 20))
    
    close_btn = pygame.Rect(box.right - 50, box.y + 15, 35, 35)
    pygame.draw.rect(game_surface, (180, 50, 50), close_btn, border_radius=6)
    x_text = small_font.render("X", True, WHITE)
    game_surface.blit(x_text, x_text.get_rect(center=close_btn.center))

    cash_rect = pygame.Rect(box.x + 40, box.y + 100, win_w - 80, 80)
    pygame.draw.rect(game_surface, (30, 35, 45), cash_rect, border_radius=8)
    game_surface.blit(small_font.render("Liquid Cash (Taxable)", True, GRAY), (cash_rect.x + 20, cash_rect.y + 15))
    game_surface.blit(small_font.render(f"${player.cash:,.2f}", True, GREEN), (cash_rect.x + 20, cash_rect.y + 45))

    off_rect = pygame.Rect(box.x + 40, box.y + 200, win_w - 80, 80)
    pygame.draw.rect(game_surface, (30, 35, 45), off_rect, border_radius=8)
    game_surface.blit(small_font.render("Offshore Account (Untouchable)", True, GRAY), (off_rect.x + 20, off_rect.y + 15))
    game_surface.blit(small_font.render(f"${player.offshore:,.2f}", True, (0, 200, 255)), (off_rect.x + 20, off_rect.y + 45))

    repat_btn = pygame.Rect(off_rect.right - 220, off_rect.y + 20, 200, 40)
    pygame.draw.rect(game_surface, (40, 100, 160) if player.offshore > 0 else (60, 60, 70), repat_btn, border_radius=6)
    r_text_font = pygame.font.Font("ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 16)
    r_text = r_text_font.render("Repatriate (10% Tax)", True, WHITE if player.offshore > 0 else GRAY)
    game_surface.blit(r_text, r_text.get_rect(center=repat_btn.center))

    tax_rect = pygame.Rect(box.x + 40, box.y + 300, win_w - 80, 80)
    pygame.draw.rect(game_surface, (45, 25, 25), tax_rect, border_radius=8)
    pygame.draw.rect(game_surface, RED, tax_rect, 1, border_radius=8)
    game_surface.blit(small_font.render("Pending Tax Liability", True, (255, 150, 150)), (tax_rect.x + 20, tax_rect.y + 15))
    game_surface.blit(small_font.render(f"${getattr(player, 'pending_tax', 0):,.2f}", True, RED), (tax_rect.x + 20, tax_rect.y + 45))

    return close_btn, repat_btn


def draw_interaction_prompt(surface, font, text, center_x, bottom_y, border_color=(80, 200, 120)):
    text_surf = font.render(text, True, (255, 255, 255))
    text_w, text_h = text_surf.get_size()
    padding_x, padding_y = 15, 6
    box_w, box_h = text_w + (padding_x * 2), text_h + (padding_y * 2)
    box_x, box_y = center_x - (box_w // 2), bottom_y - box_h
    box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
    
    pygame.draw.rect(surface, (30, 34, 45), box_rect, border_radius=6)
    pygame.draw.rect(surface, border_color, box_rect, 2, border_radius=6)
    surface.blit(text_surf, (box_x + padding_x, box_y + padding_y))


def draw_day_night_cycle(game_surface, game_clock, player, computer_rect):
    time_val = game_clock.current_time.hour + (game_clock.current_time.minute / 60.0)
    min_light = 0.35
    if 8.0 <= time_val <= 16.0: intensity = 1.0   
    elif 16.0 < time_val < 19.0: intensity = min_light + (1.0 - min_light) * (1.0 - ((time_val - 16.0) / 3.0))   
    elif 19.0 <= time_val <= 24.0 or 0.0 <= time_val <= 5.0: intensity = min_light   
    elif 5.0 < time_val < 8.0: intensity = min_light + (1.0 - min_light) * ((time_val - 5.0) / 3.0)   

    if intensity >= 0.99: return 

    r, g = int(255 * intensity), int(255 * intensity)
    b = int(255 * max(intensity, 0.55)) 
    overlay = pygame.Surface(game_surface.get_size())
    overlay.fill((r, g, b))

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

        draw_light((player.x + 44, player.y + 40), 160, (glow_max, glow_max, int(glow_max * 0.8)))
        if computer_rect: draw_light(computer_rect.center, 140, (int(glow_max * 0.5), int(glow_max * 0.9), glow_max)) 

    game_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_MULT)


def draw_portfolio_screen(game_surface, title_font, body_font, small_font, player, stocks, scroll_y, active_tab="Holdings"):
    from .constants import GOLD, WHITE, GRAY, GREEN, RED
    
    win_w, win_h = 880, 550
    win_x, win_y = (game_surface.get_width() - win_w) // 2, (game_surface.get_height() - win_h) // 2
    box = pygame.Rect(win_x, win_y, win_w, win_h)
    
    pygame.draw.rect(game_surface, (20, 24, 32), box, border_radius=12)
    pygame.draw.rect(game_surface, (50, 130, 255), box, 2, border_radius=12)
    
    title = body_font.render("[ PERSONAL PORTFOLIO ]", True, GOLD)
    game_surface.blit(title, (box.x + 30, box.y + 20))
    close_btn = draw_close_button(game_surface, box.right - 50, box.y + 15, small_font)

    stock_dict = {s.name: s for s in stocks}
    total_stock_value = 0
    total_initial_cost = 0
    holdings = []
    
    if hasattr(player, 'portfolio'):
        for ticker, shares in player.portfolio.items():
            if shares > 0 and ticker in stock_dict:
                current_price = stock_dict[ticker].price
                live_value = shares * current_price
                total_stock_value += live_value
                avg_cost = player.cost_basis.get(ticker, current_price) if hasattr(player, 'cost_basis') else current_price
                initial_cost = shares * avg_cost
                total_initial_cost += initial_cost
                pnl = live_value - initial_cost
                pnl_pct = (pnl / initial_cost * 100) if initial_cost > 0 else 0
                
                holdings.append({
                    "ticker": ticker, "shares": shares, "price": current_price, 
                    "avg_cost": avg_cost, "value": live_value, "pnl": pnl, "pnl_pct": pnl_pct
                })
                
    holdings.sort(key=lambda x: x["value"], reverse=True)
    net_worth = player.cash + total_stock_value + player.offshore - player.owed_taxes

    total_realized_pnl = 0
    if hasattr(player, 'trade_history'):
        for trade in player.trade_history:
            if trade["action"] in ["SELL", "FINE", "TAX", "WIRE", "REPAT"]: 
                total_realized_pnl += trade.get("pnl", 0)
    stats_rect = pygame.Rect(box.x + 30, box.y + 70, win_w - 60, 90)
    pygame.draw.rect(game_surface, (30, 35, 45), stats_rect, border_radius=8)
    
    game_surface.blit(small_font.render("Total Net Worth", True, GRAY), (stats_rect.x + 20, stats_rect.y + 15))
    nw_sign = "-" if net_worth < 0 else ""
    game_surface.blit(small_font.render(f"{nw_sign}${abs(net_worth):,.2f}", True, GREEN if net_worth >= 0 else RED), (stats_rect.x + 20, stats_rect.y + 45))
    
    global_pnl = total_stock_value - total_initial_cost
    global_pnl_pct = (global_pnl / total_initial_cost * 100) if total_initial_cost > 0 else 0
    pnl_color = GREEN if global_pnl >= 0 else RED
    g_sign = "+" if global_pnl >= 0 else "-"
    
    game_surface.blit(small_font.render("Unrealized P&L", True, GRAY), (stats_rect.x + 240, stats_rect.y + 15))
    game_surface.blit(small_font.render(f"{g_sign}${abs(global_pnl):,.2f} ({g_sign}{abs(global_pnl_pct):.1f}%)", True, pnl_color), (stats_rect.x + 240, stats_rect.y + 45))

    r_sign = "+" if total_realized_pnl >= 0 else "-"
    r_color = GREEN if total_realized_pnl >= 0 else RED
    game_surface.blit(small_font.render("Realized P&L", True, GRAY), (stats_rect.x + 480, stats_rect.y + 15))
    game_surface.blit(small_font.render(f"{r_sign}${abs(total_realized_pnl):,.2f}", True, r_color), (stats_rect.x + 480, stats_rect.y + 45))

    game_surface.blit(small_font.render("Liquid Cash", True, GRAY), (stats_rect.x + 680, stats_rect.y + 15))
    game_surface.blit(small_font.render(f"${player.cash:,.2f}", True, GOLD), (stats_rect.x + 680, stats_rect.y + 45))

    holdings_btn = pygame.Rect(box.x + 30, box.y + 175, 120, 30)
    history_btn = pygame.Rect(box.x + 160, box.y + 175, 120, 30)

    h_col = (50, 130, 255) if active_tab == "Holdings" else (40, 45, 60)
    pygame.draw.rect(game_surface, h_col, holdings_btn, border_radius=6)
    game_surface.blit(small_font.render("Holdings", True, WHITE), (holdings_btn.x + 25, holdings_btn.y + 6))

    hist_col = (50, 130, 255) if active_tab == "History" else (40, 45, 60)
    pygame.draw.rect(game_surface, hist_col, history_btn, border_radius=6)
    game_surface.blit(small_font.render("History", True, WHITE), (history_btn.x + 30, history_btn.y + 6))

    list_rect = pygame.Rect(box.x + 30, box.y + 215, win_w - 60, win_h - 245)
    game_surface.set_clip(list_rect)
    row_y = list_rect.y + scroll_y
    items_count = 0

    if active_tab == "Holdings":
        if not holdings:
            empty_text = small_font.render("Your portfolio is empty. Go trade some stocks!", True, GRAY)
            game_surface.blit(empty_text, empty_text.get_rect(center=list_rect.center))
        else:
            items_count = len(holdings)
            for item in holdings:
                row_rect = pygame.Rect(box.x + 30, row_y, win_w - 60, 45)
                if row_rect.bottom > list_rect.top and row_rect.top < list_rect.bottom:
                    pygame.draw.rect(game_surface, (38, 42, 55), row_rect, border_radius=6)
                    game_surface.blit(small_font.render(item["ticker"], True, WHITE), (row_rect.x + 15, row_rect.y + 12))
                    game_surface.blit(small_font.render(f"{item['shares']} shrs @ ${item['avg_cost']:.2f}", True, GRAY), (row_rect.x + 110, row_rect.y + 12))
                    val_surf = small_font.render(f"Value: ${item['value']:,.2f}", True, WHITE)
                    game_surface.blit(val_surf, (row_rect.x + 340, row_rect.y + 12))
                    
                    item_sign = "+" if item["pnl"] >= 0 else "-"
                    item_color = GREEN if item["pnl"] >= 0 else RED
                    pnl_surf = small_font.render(f"{item_sign}${abs(item['pnl']):,.2f} ({item_sign}{abs(item['pnl_pct']):.1f}%)", True, item_color)
                    game_surface.blit(pnl_surf, (row_rect.right - pnl_surf.get_width() - 15, row_rect.y + 12))
                row_y += 50

    elif active_tab == "History":
        history = getattr(player, 'trade_history', [])
        if not history:
            empty_text = small_font.render("No trades executed yet.", True, GRAY)
            game_surface.blit(empty_text, empty_text.get_rect(center=list_rect.center))
        else:
            items_count = len(history)
            for item in reversed(history): 
                row_rect = pygame.Rect(box.x + 30, row_y, win_w - 60, 45)
                if row_rect.bottom > list_rect.top and row_rect.top < list_rect.bottom:
                    pygame.draw.rect(game_surface, (38, 42, 55), row_rect, border_radius=6)
                    
                    action_col = GREEN if item["action"] in ["BUY", "REPAT"] else RED
                    game_surface.blit(small_font.render(item["action"], True, action_col), (row_rect.x + 15, row_rect.y + 12))
                    game_surface.blit(small_font.render(item["ticker"], True, WHITE), (row_rect.x + 85, row_rect.y + 12))
                    
                    if item["action"] in ["FINE", "TAX", "WIRE", "REPAT"]:
                        if item["action"] in ["FINE", "TAX"]:
                            lbl, lbl_col = "FEDERAL DEDUCTION", (180, 60, 60)
                        elif item["action"] == "WIRE":
                            lbl, lbl_col = "FUNDS HIDDEN", (180, 60, 60)
                        else:
                            lbl, lbl_col = "FUNDS REPATRIATED", (60, 180, 60)
                        game_surface.blit(small_font.render(lbl, True, lbl_col), (row_rect.x + 160, row_rect.y + 12))
                    else:
                        game_surface.blit(small_font.render(f"{item['shares']} @ ${item['price']:.2f}", True, GRAY), (row_rect.x + 160, row_rect.y + 12))
                    
                    tot_surf = small_font.render(f"Total: ${item['total']:,.2f}", True, WHITE)
                    game_surface.blit(tot_surf, (row_rect.x + 400, row_rect.y + 12))
                    
                    if item["action"] in ["SELL", "FINE", "TAX", "WIRE", "REPAT"]:
                        h_sign = "+" if item["pnl"] >= 0 else "-"
                        pnl_color = GREEN if item["pnl"] >= 0 else RED
                        pnl_surf = small_font.render(f"{h_sign}${abs(item['pnl']):,.2f} P&L", True, pnl_color)
                        game_surface.blit(pnl_surf, (row_rect.right - pnl_surf.get_width() - 15, row_rect.y + 12))
                row_y += 50

    game_surface.set_clip(None)
    max_scroll = min(0, list_rect.height - (items_count * 50))
    return close_btn, max_scroll, holdings_btn, history_btn


# ==========================================================
# SETTINGS SYSTEM
# ==========================================================
_settings_open = False
settings_tab = "Audio"  
_music_volume = 0.6
_sfx_volume = 0.7
_brightness = 1.0
_show_controls = False

def open_settings():
    global _settings_open
    _settings_open = True

def close_settings():
    global _settings_open, _show_controls
    _settings_open = False
    _show_controls = False

def is_settings_open():
    return _settings_open

def get_music_volume(): return _music_volume
def get_sfx_volume(): return _sfx_volume
def get_brightness(): return _brightness

def apply_brightness_overlay(game_surface):
    if _brightness >= 1.0: return
    darkness = int((1.0 - _brightness) * 180)
    overlay = pygame.Surface(game_surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, darkness))
    game_surface.blit(overlay, (0, 0))

def draw_settings_overlay(game_surface, title_font, body_font, small_font, game_mouse, mouse_down):
    global _music_volume, _sfx_volume, _brightness, _show_controls, settings_tab

    overlay = pygame.Surface(game_surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    game_surface.blit(overlay, (0, 0))

    win_w, win_h = 700, 520
    win_x, win_y = (GAME_W - win_w) // 2, (GAME_H - win_h) // 2
    panel = pygame.Rect(win_x, win_y, win_w, win_h)

    pygame.draw.rect(game_surface, (25, 30, 45), panel, border_radius=12)
    pygame.draw.rect(game_surface, GOLD, panel, 2, border_radius=12)

    title = body_font.render("[ SETTINGS ]", True, GOLD)
    game_surface.blit(title, (panel.x + 30, panel.y + 20))
    close_btn = draw_close_button(game_surface, panel.right - 55, panel.y + 15, small_font)

    section_y = panel.y + 90
    labels = [("Music Volume", _music_volume), ("SFX Volume", _sfx_volume), ("Brightness", _brightness)]
    buttons = {}

    for i, (label, value) in enumerate(labels):
        y = section_y + (i * 90)
        label_surf = body_font.render(label, True, WHITE)
        game_surface.blit(label_surf, (panel.x + 40, y))

        minus_btn = pygame.Rect(panel.x + 320, y - 5, 45, 45)
        draw_button(game_surface, minus_btn, "-", body_font, color=(140, 50, 50))

        bar_rect = pygame.Rect(panel.x + 390, y + 10, 180, 12)
        pygame.draw.rect(game_surface, (45, 50, 70), bar_rect, border_radius=6)
        fill_w = int(bar_rect.width * value)
        pygame.draw.rect(game_surface, GOLD, (bar_rect.x, bar_rect.y, fill_w, bar_rect.height), border_radius=6)

        plus_btn = pygame.Rect(panel.x + 590, y - 5, 45, 45)
        draw_button(game_surface, plus_btn, "+", body_font, color=(40, 130, 80))

        value_text = small_font.render(f"{int(value * 100)}%", True, WHITE)
        game_surface.blit(value_text, (panel.x + 640, y + 8))
        buttons[label] = {"minus": minus_btn, "plus": plus_btn}

    controls_btn = pygame.Rect(panel.x + 40, panel.bottom - 80, 220, 45)
    draw_button(game_surface, controls_btn, "Controls Manual", small_font, color=(70, 90, 170))

    controls_close = None
    if _show_controls:
        popup = pygame.Rect(panel.x + 230, panel.y + 160, 440, 310)
        pygame.draw.rect(game_surface, (30, 35, 50), popup, border_radius=10)
        pygame.draw.rect(game_surface, BLUE, popup, 2, border_radius=10)
        game_surface.blit(body_font.render("CONTROLS MANUAL", True, GOLD), (popup.x + 20, popup.y + 15))

        controls = [
            "WASD / Arrow Keys - Character Movement", 
            "E - Interact with Main Computer Desk", 
            "TAB - Toggle Office Furnishing Shop", 
            "T - Open Staff Recruitment Panel",
            "P - Open Personal Portfolio Dashboard",
            "N - Toggle Live Market News Feed",
            "ESC - Settings Overlay / Close active panels", 
            "Q - Force Exit Active Trade Desk Screen",
            "B - Accounts",
            "Mouse Click - Menu & Interface Buttons"
        ]
        yy = popup.y + 55
        for line in controls:
            game_surface.blit(small_font.render(line, True, WHITE), (popup.x + 20, yy))
            yy += 25
        controls_close = draw_close_button(game_surface, popup.right - 45, popup.y + 10, small_font)

    return {
        "close": close_btn,
        "music_minus": buttons["Music Volume"]["minus"], "music_plus": buttons["Music Volume"]["plus"],
        "sfx_minus": buttons["SFX Volume"]["minus"], "sfx_plus": buttons["SFX Volume"]["plus"],
        "brightness_minus": buttons["Brightness"]["minus"], "brightness_plus": buttons["Brightness"]["plus"],
        "controls": controls_btn, "controls_close": controls_close
    }

def handle_settings_click(buttons, mouse_pos):
    global _music_volume, _sfx_volume, _brightness, _show_controls
    if not buttons: return

    if _show_controls and buttons.get("controls_close"):
        if buttons["controls_close"].collidepoint(mouse_pos):
            _show_controls = False
            return
        return  

    if buttons["music_minus"].collidepoint(mouse_pos): _music_volume = max(0.0, _music_volume - 0.1)
    elif buttons["music_plus"].collidepoint(mouse_pos): _music_volume = min(1.0, _music_volume + 0.1)
    elif buttons["sfx_minus"].collidepoint(mouse_pos): _sfx_volume = max(0.0, _sfx_volume - 0.1)
    elif buttons["sfx_plus"].collidepoint(mouse_pos): _sfx_volume = min(1.0, _sfx_volume + 0.1)
    elif buttons["brightness_minus"].collidepoint(mouse_pos): _brightness = max(0.2, _brightness - 0.1)
    elif buttons["brightness_plus"].collidepoint(mouse_pos): _brightness = min(1.0, _brightness + 0.1)
    elif buttons["controls"].collidepoint(mouse_pos): _show_controls = True
    elif buttons["close"].collidepoint(mouse_pos): close_settings()