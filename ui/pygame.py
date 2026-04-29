import pygame
import sys

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

def draw_button(surf, rect, text, font, color=BLUE, text_color=WHITE, radius=8, icon=None):
    """Draw a rounded-rect button and return whether it's hovered."""
    mx, my = pygame.mouse.get_pos()
    # map real-mouse → game coords
    screen = pygame.display.get_surface()
    scale_x = GAME_W / screen.get_width()
    scale_y = GAME_H / screen.get_height()
    gx = int(mx * scale_x)
    gy = int(my * scale_y)
    
    hovered = rect.collidepoint(gx, gy)
    col = tuple(min(255, c + 40) for c in color) if hovered else color
    
    pygame.draw.rect(surf, col, rect, border_radius=radius)
    pygame.draw.rect(surf, WHITE, rect, 2, border_radius=radius)
    
    # Draw icon and text centered together
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
    """Convert a MOUSEBUTTONDOWN event to game-surface coords."""
    screen = pygame.display.get_surface()
    scale_x = GAME_W / screen.get_width()
    scale_y = GAME_H / screen.get_height()
    return int(event.pos[0] * scale_x), int(event.pos[1] * scale_y)


# ── screens ────────────────────────────────────────────────────────────────────

def draw_menu(game_surface, title_font, body_font, small_font, icon_play, icon_person, icon_quit):
    game_surface.fill(DARK)

    # subtle grid lines
    for x in range(0, GAME_W, 40):
        pygame.draw.line(game_surface, (30, 30, 55), (x, 0), (x, GAME_H))
    for y in range(0, GAME_H, 40):
        pygame.draw.line(game_surface, (30, 30, 55), (0, y), (GAME_W, y))

    # title
    title = title_font.render("HEDGE FUND", True, GOLD)
    sub   = body_font.render("The Game", True, LGRAY)
    game_surface.blit(title, title.get_rect(centerx=GAME_W // 2, y=55))
    game_surface.blit(sub,   sub.get_rect(centerx=GAME_W // 2,   y=115))

    # divider
    pygame.draw.line(game_surface, GOLD, (180, 140), (420, 140), 1)

    start_btn  = pygame.Rect(200, 165, 200, 42)
    char_btn   = pygame.Rect(200, 220, 200, 42)
    quit_btn   = pygame.Rect(200, 275, 200, 42)

    # Passing the loaded icons into the buttons! Removed text emojis.
    draw_button(game_surface, start_btn, "START  (Enter)", small_font, color=(30, 140, 80), icon=icon_play)
    draw_button(game_surface, char_btn,  "Characters",     small_font, color=(60, 80, 160), icon=icon_person)
    draw_button(game_surface, quit_btn,  "Quit  (Q)",     small_font, color=(140, 40, 40), icon=icon_quit)

    hint = small_font.render("Press ENTER to start  •  Q to quit", True, GRAY)
    game_surface.blit(hint, hint.get_rect(centerx=GAME_W // 2, y=340))

    return start_btn, char_btn, quit_btn


def draw_char_select(game_surface, title_font, body_font, small_font, selected_idx, char_images):
    game_surface.fill(DARK)
    for x in range(0, GAME_W, 40):
        pygame.draw.line(game_surface, (30, 30, 55), (x, 0), (x, GAME_H))
    for y in range(0, GAME_H, 40):
        pygame.draw.line(game_surface, (30, 30, 55), (0, y), (GAME_W, y))

    heading = title_font.render("SELECT CHARACTER", True, GOLD)
    game_surface.blit(heading, heading.get_rect(centerx=GAME_W // 2, y=18))
    pygame.draw.line(game_surface, GOLD, (100, 60), (500, 60), 1)

    card_w, card_h = 140, 200
    spacing = 20
    total_w = len(CHARACTERS) * card_w + (len(CHARACTERS) - 1) * spacing
    start_x = (GAME_W - total_w) // 2

    card_rects = []
    for i, char in enumerate(CHARACTERS):
        cx = start_x + i * (card_w + spacing)
        cy = 75
        rect = pygame.Rect(cx, cy, card_w, card_h)
        card_rects.append(rect)

        bg = PANEL if i != selected_idx else (35, 55, 100)
        border = GOLD if i == selected_idx else GRAY
        bw     = 2   if i == selected_idx else 1
        pygame.draw.rect(game_surface, bg,     rect, border_radius=10)
        pygame.draw.rect(game_surface, border, rect, bw, border_radius=10)

        # character sprite (or placeholder)
        if char_images[i]:
            img = pygame.transform.scale(char_images[i], (70, 120))
            game_surface.blit(img, img.get_rect(centerx=rect.centerx, y=cy + 10))
        else:
            placeholder = pygame.Rect(rect.centerx - 30, cy + 10, 60, 110)
            pygame.draw.rect(game_surface, (60, 60, 80), placeholder, border_radius=6)
            p_label = small_font.render("?", True, LGRAY)
            game_surface.blit(p_label, p_label.get_rect(center=placeholder.center))

        name_surf = body_font.render(char["name"], True, WHITE if i == selected_idx else LGRAY)
        desc_surf = small_font.render(char["desc"], True, GRAY)
        game_surface.blit(name_surf, name_surf.get_rect(centerx=rect.centerx, y=cy + 140))
        game_surface.blit(desc_surf, desc_surf.get_rect(centerx=rect.centerx, y=cy + 162))

    back_btn    = pygame.Rect(30,  355, 120, 36)
    confirm_btn = pygame.Rect(450, 355, 120, 36)
    draw_button(game_surface, back_btn,    "← Back",    small_font, color=(80, 40, 80))
    draw_button(game_surface, confirm_btn, "Confirm ✓", small_font, color=(30, 140, 80))

    hint = small_font.render("Click a character  •  Enter to confirm  •  Q / Esc to go back", True, GRAY)
    game_surface.blit(hint, hint.get_rect(centerx=GAME_W // 2, y=320))

    return card_rects, back_btn, confirm_btn


# ── main loop ──────────────────────────────────────────────────────────────────

def run(game):
    pygame.init()

    display_info  = pygame.display.Info()
    SCREEN_W, SCREEN_H = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN)
    pygame.display.set_caption("Hedge Fund Game")

    game_surface = pygame.Surface((GAME_W, GAME_H))

    # fonts
    title_font = pygame.font.SysFont("Arial Black", 40, bold=True)
    body_font  = pygame.font.SysFont(None, 28)
    small_font = pygame.font.SysFont(None, 22)
    hud_font   = pygame.font.SysFont(None, 26)

    # load assets (graceful fallback)
    try:
        background = pygame.image.load("office_bg.png").convert()
    except Exception:
        background = pygame.Surface((GAME_W, GAME_H))
        background.fill((30, 40, 60))

    char_images = []
    for c in CHARACTERS:
        try:
            img = pygame.image.load(c["file"]).convert_alpha()
            char_images.append(img)
        except Exception:
            char_images.append(None)

    # --- Load UI Icons ---
    try:
        icon_coin = pygame.image.load("ui/assets/coin.png").convert_alpha()
        icon_coin = pygame.transform.scale(icon_coin, (24, 24))
    except Exception:
        icon_coin = None

    try:
        icon_play = pygame.image.load("ui/assets/play.png").convert_alpha()
        icon_play = pygame.transform.scale(icon_play, (20, 20))
    except Exception:
        icon_play = None

    try:
        icon_person = pygame.image.load("ui/assets/person.png").convert_alpha()
        icon_person = pygame.transform.scale(icon_person, (20, 20))
    except Exception:
        icon_person = None
    try:
        icon_quit = pygame.image.load("ui/assets/quit.png").convert_alpha()
        icon_quit = pygame.transform.scale(icon_quit, (20, 20))
    except Exception:
        icon_quit = None


    clock          = pygame.time.Clock()
    move_speed     = 5
    player         = game.players[0]
    computer_rect  = pygame.Rect(100, 250, 60, 20)
    interaction_distance = 80

    market_open    = False
    last_update    = pygame.time.get_ticks()
    state          = "menu"
    selected_char  = 0
    running        = True

    # HUD button
    menu_btn_rect = pygame.Rect(GAME_W - 90, 8, 80, 28)

    while running:

        # ── EVENTS ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # global quit keys
                if event.key in (pygame.K_q, pygame.K_ESCAPE) and state != "game":
                    if state == "char_select":
                        state = "menu"
                    else:
                        running = False

                elif state == "menu":
                    if event.key == pygame.K_RETURN:
                        state = "game"

                elif state == "char_select":
                    if event.key == pygame.K_RETURN:
                        state = "menu"
                    elif event.key == pygame.K_LEFT:
                        selected_char = (selected_char - 1) % len(CHARACTERS)
                    elif event.key == pygame.K_RIGHT:
                        selected_char = (selected_char + 1) % len(CHARACTERS)

                elif state == "game":
                    if event.key == pygame.K_ESCAPE:
                        state = "menu"
                        market_open = False
                    elif event.key == pygame.K_e and not market_open:
                        player_rect = pygame.Rect(player.x, player.y, 100, 200)
                        dx = abs(player_rect.centerx - computer_rect.centerx)
                        dy = abs(player_rect.centery - computer_rect.centery)
                        if dx < interaction_distance and dy < interaction_distance:
                            market_open = True
                    elif event.key == pygame.K_q and market_open:
                        market_open = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gx, gy = mouse_clicked_in_game(event, game_surface)
                gpt    = (gx, gy)

                if state == "menu":
                    start_btn, char_btn, quit_btn = _last_menu_rects
                    if start_btn.collidepoint(gpt):
                        state = "game"
                    elif char_btn.collidepoint(gpt):
                        state = "char_select"
                    elif quit_btn.collidepoint(gpt):
                        running = False

                elif state == "char_select":
                    card_rects, back_btn, confirm_btn = _last_char_rects
                    for i, r in enumerate(card_rects):
                        if r.collidepoint(gpt):
                            selected_char = i
                    if back_btn.collidepoint(gpt):
                        state = "menu"
                    elif confirm_btn.collidepoint(gpt):
                        state = "menu"

                elif state == "game":
                    if menu_btn_rect.collidepoint(gpt):
                        state = "menu"
                        market_open = False

        # ── DRAW ──────────────────────────────────────────────────────────────
        game_surface.fill(DARK)

        if state == "menu":
            _last_menu_rects = draw_menu(game_surface, title_font, body_font, small_font, icon_play, icon_person, icon_quit)
            _last_char_rects = ([], pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0))

        elif state == "char_select":
            _last_char_rects = draw_char_select(
                game_surface, title_font, body_font, small_font, selected_char, char_images)
            _last_menu_rects = (pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0))

        elif state == "game":
            _last_menu_rects = (pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0))
            _last_char_rects = ([], pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0))

            # stock update
            now = pygame.time.get_ticks()
            if now - last_update > 1000:
                game.update_stocks()
                last_update = now

            game_surface.blit(background, (0, 0))

            # HUD (Using the coin image here!)
            cash_text = hud_font.render(f"${player.cash:,.0f}", True, GOLD)
            if icon_coin:
                game_surface.blit(icon_coin, (12, 10))
                game_surface.blit(cash_text, (40, 12)) # shifted over to make room for icon
            else:
                game_surface.blit(cash_text, (12, 12))

            draw_button(game_surface, menu_btn_rect, "≡ Menu", small_font,
                        color=(40, 40, 80), text_color=LGRAY)

            # player
            player_rect = pygame.Rect(player.x, player.y, 100, 200)
            char_img = char_images[selected_char]
            if char_img:
                scaled_img = pygame.transform.scale(char_img, (100, 200))
                game_surface.blit(scaled_img, player_rect)
            else:
                pygame.draw.rect(game_surface, (80, 80, 120), player_rect, border_radius=8)

            # proximity prompt
            dx = abs(player_rect.centerx - computer_rect.centerx)
            dy = abs(player_rect.centery - computer_rect.centery)
            near_computer = dx < interaction_distance and dy < interaction_distance
            if near_computer and not market_open:
                prompt = hud_font.render("Press E to interact", True, GREEN)
                game_surface.blit(prompt, (computer_rect.x - 10, computer_rect.y - 40))

            # movement
            if not market_open:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    player.move(-move_speed)
                elif keys[pygame.K_d]:
                    player.move(move_speed)

            # market overlay
            if market_open:
                box = pygame.Rect(70, 80, 460, 240)
                overlay = pygame.Surface((box.width, box.height), pygame.SRCALPHA)
                
                # Correctly drawing the rounded background
                pygame.draw.rect(overlay, (10, 10, 30, 220), overlay.get_rect(), border_radius=12)
                game_surface.blit(overlay, (box.x, box.y))
                pygame.draw.rect(game_surface, BLUE, box, 2, border_radius=12)

                # Removed the broken chart emoji here
                header = body_font.render("Stock Market", True, GOLD)
                game_surface.blit(header, (box.x + 16, box.y + 14))
                pygame.draw.line(game_surface, (60, 80, 140),
                                 (box.x + 10, box.y + 40), (box.x + box.width - 10, box.y + 40))

                row_y = box.y + 52
                for stock in game.stocks:
                    color = GREEN if getattr(stock, 'trend', 0) >= 0 else RED
                    line  = hud_font.render(f"  {stock.name:<12}  ${stock.price:>8.2f}", True, color)
                    game_surface.blit(line, (box.x + 16, row_y))
                    row_y += 32

                close = small_font.render("Press Q to close", True, GRAY)
                game_surface.blit(close, (box.x + 16, box.y + box.height - 28))

            # ESC hint
            hint = small_font.render("ESC → Menu", True, GRAY)
            game_surface.blit(hint, (12, GAME_H - 22))

        # ── SCALE & FLIP ──────────────────────────────────────────────────────
        scaled = pygame.transform.scale(game_surface, (SCREEN_W, SCREEN_H))
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()