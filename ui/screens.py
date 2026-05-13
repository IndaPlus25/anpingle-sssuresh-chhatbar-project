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

def draw_market_overlay(game_surface, body_font, hud_font, small_font, stocks):
    """Draws the Stock Market interaction menu."""
    from .constants import BLUE, GOLD, GREEN, GRAY
    
    box = pygame.Rect(140, 160, 1000, 400)
    pygame.draw.rect(game_surface, (10, 10, 30), box, border_radius=12)
    pygame.draw.rect(game_surface, BLUE, box, 2, border_radius=12)
    
    title = body_font.render("STOCK MARKET", True, GOLD)
    game_surface.blit(title, (box.x + 30, box.y + 20))
    
    row_y = box.y + 80
    for s in stocks:
        game_surface.blit(hud_font.render(f"{s.name:<12} ${s.price:>8.2f}", True, GREEN), (box.x + 30, row_y))
        row_y += 50
        
    close_hint = small_font.render("Press Q to close", True, GRAY)
    game_surface.blit(close_hint, (box.x + 30, box.y + box.height - 40))
def draw_shop_overlay(game_surface, body_font, small_font, player, icon_coin, desks_assets, owned_desks, current_desk_id):
    """shop overlay"""
    from .constants import BLUE, GOLD, GREEN, GRAY, PANEL, WHITE, SHOP_ITEMS
    
    win_w, win_h = 700, 500
    win_x, win_y = (game_surface.get_width() - win_w) // 2, (game_surface.get_height() - win_h) // 2
    box = pygame.Rect(win_x, win_y, win_w, win_h)
    
    pygame.draw.rect(game_surface, (40, 45, 60), box, border_radius=8)
    pygame.draw.rect(game_surface, PANEL, box.inflate(-10, -50), border_radius=4)
    
    title = body_font.render("Shop - Upgrades", True, WHITE)
    game_surface.blit(title, (box.x + 20, box.y + 10))
    close_hint = small_font.render("Press ESC to close", True, GRAY)
    game_surface.blit(close_hint, (box.x + win_w - close_hint.get_width() - 20, box.y + 15))

    buy_buttons = []
    row_y = win_y + 60
    
    for item in SHOP_ITEMS:
        row_rect = pygame.Rect(win_x + 20, row_y, win_w - 40, 70)
        pygame.draw.rect(game_surface, (35, 40, 55), row_rect, border_radius=6)
        pygame.draw.rect(game_surface, (50, 60, 80), row_rect, 1, border_radius=6)
        
        # Draw Thumbnail Image
        desk_img = desks_assets.get(item["id"])
        if desk_img:
            # Scale it down for the list view
            thumb = pygame.transform.scale(desk_img, (75, 55))
            game_surface.blit(thumb, (row_rect.x + 10, row_rect.y + 5))
        
        # Item Name
        name_text = small_font.render(item["name"], True, WHITE)
        game_surface.blit(name_text, (row_rect.x + 100, row_rect.y + 3))
        
        # Price
        if icon_coin:
            game_surface.blit(icon_coin, (row_rect.x + 100, row_rect.y + 30))
        price_text = small_font.render(f"${item['price']:,}", True, GOLD)
        game_surface.blit(price_text, (row_rect.x + 140, row_rect.y + 33))
        
        # Button
        btn_rect = pygame.Rect(row_rect.right - 140, row_rect.y + 15, 120, 40)
        is_owned = item["id"] in owned_desks
        is_equipped = item["id"] == current_desk_id
        
        if is_equipped:
            btn_text = "Equipped"
            btn_color = GRAY
        elif is_owned:
            btn_text = "Equip"
            btn_color = BLUE
        else:
            can_afford = player.cash >= item["price"]
            btn_text = "Buy"
            btn_color = GREEN if can_afford else (140, 40, 40)
        
        draw_button(game_surface, btn_rect, btn_text, small_font, color=btn_color)

        buy_buttons.append((btn_rect, item, btn_text)) 
        
        row_y += 85 
        
    return buy_buttons


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