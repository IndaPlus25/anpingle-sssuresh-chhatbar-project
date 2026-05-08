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
    
    # ═══════════════════════════════════════════════════════════
    # RENDER ACTIVE EMPLOYEES
    # ═══════════════════════════════════════════════════════════
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