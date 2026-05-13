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
    
def draw_shop_overlay(game_surface, body_font, small_font, player, icon_coin, thumbnails, owned_items, equipped_items, shop_tab, scroll_y):
    """Draws the scrollable, tabbed shop overlay."""
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