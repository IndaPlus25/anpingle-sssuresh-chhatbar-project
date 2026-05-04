import pygame
import sys
import os

GAME_W, GAME_H = 600, 400

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (255, 0,   0)
GREEN  = (0,   200, 100)
BLUE   = (50,  130, 255)
DARK   = (15,  15,  30)
PANEL  = (25,  25,  50)
GOLD   = (255, 210, 60)
GRAY   = (140, 140, 160)
LGRAY  = (200, 200, 220)

CHARACTERS = [
    {"name": "Alex",   "file": "ui/characters/char1.png", "desc": "Balanced trader"},
    {"name": "Morgan", "file": "ui/characters/char2.png", "desc": "Risk taker"},
    {"name": "Jordan", "file": "ui/characters/char3.png", "desc": "Market analyst"},
]

# ── helpers ────────────────────────────────────────────────────────────────────

def load_8way_animations(base_path):
    """Loads 8-directional idle and walking frames from the character folder structure."""
    directions = ['north', 'south', 'east', 'west', 'northeast', 'northwest', 'southeast', 'southwest']
    animations = {"idle": {}, "walk": {}}
    
    for d in directions:
        try:
            animations["idle"][d] = pygame.image.load(f"{base_path}/{d}.png").convert_alpha()
        except:
            animations["idle"][d] = None
            
        walk_frames = []
        for i in range(6):
            try:
                img_path = f"{base_path}/walk/walk{d}/f{i}.png"
                img = pygame.image.load(img_path).convert_alpha()
                walk_frames.append(img)
            except:
                break
        animations["walk"][d] = walk_frames
    return animations

def draw_button(surf, rect, text, font, color=BLUE, text_color=WHITE, radius=8, icon=None):
    mx, my = pygame.mouse.get_pos()
    screen = pygame.display.get_surface()
    scale_x = GAME_W / screen.get_width()
    scale_y = GAME_H / screen.get_height()
    gx, gy = int(mx * scale_x), int(my * scale_y)
    
    hovered = rect.collidepoint(gx, gy)
    col = tuple(min(255, c + 40) for c in color) if hovered else color
    
    pygame.draw.rect(surf, col, rect, border_radius=radius)
    pygame.draw.rect(surf, WHITE, rect, 2, border_radius=radius)
    
    if icon:
        text_surf = font.render(text, True, text_color)
        total_w = icon.get_width() + 10 + text_surf.get_width()
        start_x = rect.centerx - total_w // 2
        surf.blit(icon, (start_x, rect.centery - icon.get_height() // 2))
        surf.blit(text_surf, (start_x + icon.get_width() + 10, rect.centery - text_surf.get_height() // 2))
    else:
        label = font.render(text, True, text_color)
        surf.blit(label, label.get_rect(center=rect.center))
        
    return hovered

def mouse_clicked_in_game(event, game_surface):
    screen = pygame.display.get_surface()
    scale_x = GAME_W / screen.get_width()
    scale_y = GAME_H / screen.get_height()
    return int(event.pos[0] * scale_x), int(event.pos[1] * scale_y)

# ── screens ────────────────────────────────────────────────────────────────────

def draw_menu(game_surface, title_font, body_font, small_font, icon_play, icon_person, icon_quit):
    game_surface.fill(DARK)
    for x in range(0, GAME_W, 40): pygame.draw.line(game_surface, (30, 30, 55), (x, 0), (x, GAME_H))
    for y in range(0, GAME_H, 40): pygame.draw.line(game_surface, (30, 30, 55), (0, y), (GAME_W, y))

    title = title_font.render("HEDGE FUND", True, GOLD)
    sub   = body_font.render("The Game", True, LGRAY)
    game_surface.blit(title, title.get_rect(centerx=GAME_W // 2, y=55))
    game_surface.blit(sub,   sub.get_rect(centerx=GAME_W // 2,   y=115))
    pygame.draw.line(game_surface, GOLD, (180, 140), (420, 140), 1)

    start_btn = pygame.Rect(200, 165, 200, 42)
    char_btn  = pygame.Rect(200, 220, 200, 42)
    quit_btn  = pygame.Rect(200, 275, 200, 42)

    draw_button(game_surface, start_btn, "START  (Enter)", small_font, color=(30, 140, 80), icon=icon_play)
    draw_button(game_surface, char_btn,  "Characters",     small_font, color=(60, 80, 160), icon=icon_person)
    draw_button(game_surface, quit_btn,  "Quit  (Q)",      small_font, color=(140, 40, 40), icon=icon_quit)

    return start_btn, char_btn, quit_btn

def draw_char_select(game_surface, title_font, body_font, small_font, selected_idx, all_anims, char_images):
    game_surface.fill(DARK)
    heading = title_font.render("SELECT CHARACTER", True, GOLD)
    game_surface.blit(heading, heading.get_rect(centerx=GAME_W // 2, y=18))
    
    card_w, card_h = 140, 200
    spacing = 20
    start_x = (GAME_W - (len(CHARACTERS) * card_w + (len(CHARACTERS)-1) * spacing)) // 2

    card_rects = []
    for i, char in enumerate(CHARACTERS):
        rect = pygame.Rect(start_x + i * (card_w + spacing), 75, card_w, card_h)
        card_rects.append(rect)
        bg = PANEL if i != selected_idx else (35, 55, 100)
        pygame.draw.rect(game_surface, bg, rect, border_radius=10)
        
        # Use South Idle image if available, otherwise original file
        display_img = None
        if i < len(all_anims) and all_anims[i]["idle"].get("south"):
            display_img = all_anims[i]["idle"]["south"]
        else:
            display_img = char_images[i]

        if display_img:
            img = pygame.transform.scale(display_img, (70, 120))
            game_surface.blit(img, img.get_rect(centerx=rect.centerx, y=85))
            
        name_surf = body_font.render(char["name"], True, WHITE if i == selected_idx else LGRAY)
        game_surface.blit(name_surf, name_surf.get_rect(centerx=rect.centerx, y=215))

    back_btn = pygame.Rect(30, 355, 120, 36)
    confirm_btn = pygame.Rect(450, 355, 120, 36)
    draw_button(game_surface, back_btn, "← Back", small_font, color=(80, 40, 80))
    draw_button(game_surface, confirm_btn, "Confirm ✓", small_font, color=(30, 140, 80))
    return card_rects, back_btn, confirm_btn

# ── main loop ──────────────────────────────────────────────────────────────────

def run(game):
    pygame.init()
    display_info = pygame.display.Info()
    screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
    SCREEN_W, SCREEN_H = display_info.current_w, display_info.current_h
    game_surface = pygame.Surface((GAME_W, GAME_H))

    title_font = pygame.font.SysFont("Arial Black", 40, bold=True)
    body_font  = pygame.font.SysFont(None, 28)
    small_font = pygame.font.SysFont(None, 22)
    hud_font   = pygame.font.SysFont(None, 26)

    try: background = pygame.image.load("office_bg.png").convert()
    except: background = pygame.Surface((GAME_W, GAME_H)); background.fill((30, 40, 60))

    char_images = []
    for c in CHARACTERS:
        try: char_images.append(pygame.image.load(c["file"]).convert_alpha())
        except: char_images.append(None)

    # Load 8-way animations for all characters
    all_char_anims = [
        load_8way_animations("ui/characters/char1"),
        load_8way_animations("ui/characters/char2"),
        load_8way_animations("ui/characters/char3")
    ]
    
    anim_frame = 0

    try:
        icon_coin = pygame.transform.scale(pygame.image.load("ui/assets/coin.png").convert_alpha(), (24, 24))
        icon_play = pygame.transform.scale(pygame.image.load("ui/assets/play.png").convert_alpha(), (20, 20))
        icon_person = pygame.transform.scale(pygame.image.load("ui/assets/person.png").convert_alpha(), (20, 20))
        icon_quit = pygame.transform.scale(pygame.image.load("ui/assets/quit.png").convert_alpha(), (20, 20))
    except: icon_coin = icon_play = icon_person = icon_quit = None

    clock = pygame.time.Clock()
    player = game.players[0]
    move_speed = 1.75
    computer_rect = pygame.Rect(100, 250, 60, 20)
    interaction_distance = 60 
    market_open = False
    last_update = pygame.time.get_ticks()
    state = "menu"
    selected_char = 0
    running = True
    menu_btn_rect = pygame.Rect(GAME_W - 90, 8, 80, 28)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE) and state != "game":
                    if state == "char_select": state = "menu"
                    else: running = False
                elif state == "menu" and event.key == pygame.K_RETURN: state = "game"
                elif state == "char_select":
                    if event.key == pygame.K_RETURN: state = "menu"
                    elif event.key == pygame.K_LEFT: selected_char = (selected_char - 1) % len(CHARACTERS)
                    elif event.key == pygame.K_RIGHT: selected_char = (selected_char + 1) % len(CHARACTERS)
                elif state == "game":
                    if event.key == pygame.K_ESCAPE: state = "menu"; market_open = False
                    elif event.key == pygame.K_q and market_open: 
                        market_open = False
                    elif event.key == pygame.K_e and not market_open:
                        p_rect = pygame.Rect(player.x, player.y, 40, 40)
                        if p_rect.colliderect(computer_rect.inflate(interaction_distance, interaction_distance)):
                            market_open = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gpt = mouse_clicked_in_game(event, game_surface)
                if state == "menu":
                    s, c, q = draw_menu(game_surface, title_font, body_font, small_font, icon_play, icon_person, icon_quit)
                    if s.collidepoint(gpt): state = "game"
                    elif c.collidepoint(gpt): state = "char_select"
                    elif q.collidepoint(gpt): running = False
                elif state == "char_select":
                    cards, b, conf = draw_char_select(game_surface, title_font, body_font, small_font, selected_char, all_char_anims, char_images)
                    for i, r in enumerate(cards):
                        if r.collidepoint(gpt): selected_char = i
                    if b.collidepoint(gpt): state = "menu"
                    elif conf.collidepoint(gpt): state = "menu"
                elif state == "game" and menu_btn_rect.collidepoint(gpt):
                    state = "menu"; market_open = False

        game_surface.fill(DARK)

        if state == "menu":
            draw_menu(game_surface, title_font, body_font, small_font, icon_play, icon_person, icon_quit)
        elif state == "char_select":
            draw_char_select(game_surface, title_font, body_font, small_font, selected_char, all_char_anims, char_images)
        elif state == "game":
            if pygame.time.get_ticks() - last_update > 1000:
                game.update_stocks(); last_update = pygame.time.get_ticks()

            game_surface.blit(background, (0, 0))
            
            # HUD
            if icon_coin: game_surface.blit(icon_coin, (12, 10))
            game_surface.blit(hud_font.render(f"${player.cash:,.0f}", True, GOLD), (40, 12))
            draw_button(game_surface, menu_btn_rect, "≡ Menu", small_font, color=(40, 40, 80), text_color=LGRAY)

            # Movement & Animation Logic
            dx, dy = 0, 0
            if not market_open:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]: dx = -move_speed
                if keys[pygame.K_d]: dx = move_speed
                if keys[pygame.K_w]: dy = -move_speed
                if keys[pygame.K_s]: dy = move_speed
                
                player.x = max(0, min(player.x + dx, GAME_W - 40))
                player.y = max(0, min(player.y + dy, GAME_H - 40))

                if dx != 0 or dy != 0:
                    player.is_moving = True
                    dir_str = ""
                    if dy < 0: dir_str += "north"
                    elif dy > 0: dir_str += "south"
                    if dx < 0: dir_str += "west"
                    elif dx > 0: dir_str += "east"
                    player.direction = dir_str
                    anim_frame = (anim_frame + 0.12) % 6
                else:
                    player.is_moving = False
                    anim_frame = 0

            # Draw Player
            p_rect = pygame.Rect(player.x, player.y, 40, 40)
            
            # Dynamic Animation Set Selection
            current_anims = all_char_anims[selected_char]

            if current_anims:
                d = getattr(player, 'direction', 'south')
                if player.is_moving and current_anims["walk"].get(d):
                    img = current_anims["walk"][d][int(anim_frame)]
                else:
                    img = current_anims["idle"].get(d) or char_images[selected_char]
                game_surface.blit(pygame.transform.scale(img, (40, 40)), p_rect)
            else:
                img = char_images[selected_char]
                if img: game_surface.blit(pygame.transform.scale(img, (40, 40)), p_rect)

            if p_rect.colliderect(computer_rect.inflate(interaction_distance, interaction_distance)) and not market_open:
                prompt = hud_font.render("Press E to interact", True, GREEN)
                game_surface.blit(prompt, (computer_rect.x - 10, computer_rect.y - 40))

            if market_open:
                box = pygame.Rect(70, 80, 460, 240)
                pygame.draw.rect(game_surface, (10, 10, 30), box, border_radius=12)
                pygame.draw.rect(game_surface, BLUE, box, 2, border_radius=12)
                row_y = box.y + 52
                for s in game.stocks:
                    game_surface.blit(hud_font.render(f"{s.name:<12} ${s.price:>8.2f}", True, GREEN), (box.x + 16, row_y))
                    row_y += 32
                close_hint = small_font.render("Press Q to close", True, GRAY)
                game_surface.blit(close_hint, (box.x + 16, box.y + box.height - 25))

        scaled = pygame.transform.scale(game_surface, (SCREEN_W, SCREEN_H))
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()