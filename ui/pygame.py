import pygame
import sys
import random
import os

from .constants import *
from .screens import draw_menu, draw_char_select, draw_market_overlay, draw_shop_overlay, draw_confirmation_screen, draw_news_screen, draw_news_detail
from .assets.stock_assets import (
    CANDLE_COLORS, PATTERN_PROGRESS_BG, get_pattern_color, get_pattern_info
)
from .assets import stock_assets as pattern_assets
from features.interaction import mouse_clicked_in_game, draw_button
from features.hud import draw_top_bar, draw_clock_overlay
from features.assets import load_all_assets
from features.player import handle_player_movement, draw_player
from features.clock import GameClock
from game.stocks.patterns import PATTERNS as _ALL_PATTERNS
from game.news import *

# Candlestick color aliases
light_green = CANDLE_COLORS["bullish"]["body"]
dark_green  = CANDLE_COLORS["bullish"]["border"]
light_red   = CANDLE_COLORS["bearish"]["body"]
dark_red    = CANDLE_COLORS["bearish"]["border"]

black      = (0, 0, 0)
gray       = (140, 140, 160)
light_gray = (240, 240, 240)
green      = (0, 200, 100)
red        = (255, 0, 0)
blue       = (50, 130, 255)

CHART_WIDTH   = 400
CHART_HEIGHT  = 150
CHART_PADDING = 10
CANDLE_WIDTH  = 10
CANDLE_SPACING = 4

# ==========================================
# AUDIO STATE TRACKING
# ==========================================
MUSIC_BGM  = "features/music/prettyjohn1-corporate-background-music_33sec-483404.ogg"
MUSIC_NEWS = "features/music/sonican-news-music-information-epic-30-seconds-471012.ogg"
SFX_HOVER  = "features/music/finntastico-old-computer-click-152513.mp3"
SFX_CLICK  = "features/music/freesoundeffects-button-click-289742 (1).mp3"
SFX_BUY    = "features/music/freesound_community-cash-register-purchase-87313.mp3"

# Tracks which track is loaded so switch_music never reloads the same file
_CURRENTLY_PLAYING_TRACK = None


def load_sounds():
    """Load sfx into a dict. Missing files are skipped gracefully."""
    sounds = {}
    sfx_files = {
        "hover": SFX_HOVER,
        "click": SFX_CLICK,
        "buy":   SFX_BUY,
    }
    for name, path in sfx_files.items():
        if os.path.exists(path):
            try:
                sounds[name] = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"[Audio] Could not load {path}: {e}")
        else:
            print(f"[Audio] Missing sfx: {path}")

    if "hover" in sounds: sounds["hover"].set_volume(0.15)
    if "click" in sounds: sounds["click"].set_volume(0.4)
    if "buy"   in sounds: sounds["buy"].set_volume(0.6)

    return sounds


def play(sounds, name):
    """Play a sound effect by name, silently ignoring missing sounds."""
    if name in sounds:
        sounds[name].play()


def switch_music(track_name, filepath, volume=0.3):
    """
    Safe music switcher.
    - Never reloads a track that is already playing.
    - loops=-1 handles looping natively; no emergency recovery needed.
    """
    global _CURRENTLY_PLAYING_TRACK

    # Already on this track — do nothing, let pygame loop it
    if _CURRENTLY_PLAYING_TRACK == track_name:
        return

    if not os.path.exists(filepath):
        print(f"[Audio] Missing music: {filepath}")
        return

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=-1)

        _CURRENTLY_PLAYING_TRACK = track_name
        print(f"[Audio] switched → {track_name}")

    except Exception as e:
        print(f"[Audio] Music error ({track_name}): {e}")
        _CURRENTLY_PLAYING_TRACK = None


def music_play_bgm():
    switch_music("bgm", MUSIC_BGM, 0.30)


def music_play_news():
    switch_music("news", MUSIC_NEWS, 0.45)


def draw_candle(screen, x, y, ohlc, height_scale, min_price, max_price):
    open_p, high, low, close = ohlc
    chart_top = y + CHART_PADDING

    def price_to_y(price):
        return chart_top + (max_price - price) * height_scale

    open_y  = price_to_y(open_p)
    close_y = price_to_y(close)
    high_y  = price_to_y(high)
    low_y   = price_to_y(low)

    color        = light_green if close >= open_p else light_red
    border_color = dark_green  if close >= open_p else dark_red
    body_top     = min(open_y, close_y)
    body_height  = max(1, abs(close_y - open_y))

    pygame.draw.line(screen, black, (x, high_y), (x, low_y), 1)
    body_rect = pygame.Rect(x - CANDLE_WIDTH // 2, body_top, CANDLE_WIDTH, body_height)
    pygame.draw.rect(screen, color, body_rect)
    pygame.draw.rect(screen, border_color, body_rect, 1)


def draw_stock_chart(screen, font, stock, chart_x, chart_y, visible_candles=50):
    candles = stock.candles
    if not candles:
        return
    visible_candles_list = candles[-visible_candles:]
    if not visible_candles_list:
        return

    min_price   = min(c.low  for c in visible_candles_list)
    max_price   = max(c.high for c in visible_candles_list)
    price_range = max_price - min_price or 1

    chart_available_height = CHART_HEIGHT - 2 * CHART_PADDING
    height_scale = chart_available_height / price_range

    chart_rect = pygame.Rect(chart_x, chart_y, CHART_WIDTH, CHART_HEIGHT)
    pygame.draw.rect(screen, light_gray, chart_rect)
    pygame.draw.rect(screen, black, chart_rect, 1)

    grid_height        = CHART_HEIGHT - 2 * CHART_PADDING
    num_grid_lines     = 5
    total_candle_width = CANDLE_WIDTH + CANDLE_SPACING
    candle_x           = chart_x + CHART_PADDING

    for candle in visible_candles_list:
        if candle_x + CANDLE_WIDTH > chart_x + CHART_WIDTH - CHART_PADDING:
            break
        draw_candle(screen, candle_x, chart_y,
                    (candle.open, candle.high, candle.low, candle.close),
                    height_scale, min_price, max_price)
        candle_x += total_candle_width

    price_y = chart_y + CHART_PADDING
    for i in range(num_grid_lines + 1):
        price_pos = max_price - (price_range * i // num_grid_lines)
        screen.blit(font.render(f"${price_pos:.1f}", True, black),
                    (chart_x - 50, price_y - 5 + (grid_height * i // num_grid_lines)))


def draw_pattern_info(screen, font, stock, x, y):
    if stock.current_pattern_name is None:
        return
    pattern_name = stock.current_pattern_name
    pattern_info = pattern_assets.get_pattern_info(pattern_name)
    if pattern_info is None:
        return
    display_name, category, color_category = pattern_info
    color = pattern_assets.get_pattern_color(pattern_name)
    screen.blit(font.render(f"PATTERN: {display_name}", True, color), (x, y))
    screen.blit(font.render(f"CATEGORY: {category}", True, (100, 100, 100)), (x, y + 20))

    if stock._active_segment:
        remaining_ticks, _  = stock._active_segment
        total_pattern_ticks = getattr(stock, '_pattern_total_ticks', 20)
        queue_ticks         = sum(q[0] for q in stock._pattern_queue)
        completed           = max(0, total_pattern_ticks - (queue_ticks + remaining_ticks))
        progress_pct        = completed / total_pattern_ticks if total_pattern_ticks > 0 else 0
        bar_width, bar_height = 200, 12
        bar_x, bar_y = x, y + 45
        pygame.draw.rect(screen, PATTERN_PROGRESS_BG, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, black,               (bar_x, bar_y, bar_width, bar_height), 1)
        pygame.draw.rect(screen, color,               (bar_x, bar_y, int(bar_width * progress_pct), bar_height))
        num_indicators    = min(10, total_pattern_ticks)
        indicator_spacing = bar_width // num_indicators
        for i in range(num_indicators):
            indicator_x = bar_x + (i * indicator_spacing) + indicator_spacing // 2
            pygame.draw.line(screen, gray, (indicator_x, bar_y - 3), (indicator_x, bar_y + bar_height + 3), 1)
        screen.blit(font.render(f"{int(progress_pct * 100)}%", True, black), (bar_x + bar_width + 10, bar_y))


def draw_candle_progress(screen, stock, x, y, candle_width=8, spacing=3):
    if not stock.candles and stock._current_candle is None:
        return
    current = stock._current_candle
    if current is None:
        return
    candle_base_y, candle_base_x = y + 10, x
    body_height, body_width = 20, candle_width
    ticks_per_candle = 5
    progress = min(current.tick / ticks_per_candle, 1.0) if ticks_per_candle > 0 else 1.0
    alpha    = int(255 * progress)
    if current.is_bullish():   body_color = (0, min(255, 150 + 100 * progress), 0, alpha)
    elif current.is_bearish(): body_color = (min(255, 200 + 55 * progress), 0, 0, alpha)
    else:                      body_color = (128, 128, 128, alpha)
    body_rect = pygame.Rect(candle_base_x, candle_base_y - body_height, body_width, body_height)
    pygame.draw.rect(screen, body_color[:3], body_rect)
    pygame.draw.rect(screen, black, body_rect, 1)
    if progress < 1.0:
        bar_x, bar_y = candle_base_x + body_width + 5, candle_base_y - body_height // 2
        pygame.draw.rect(screen, PATTERN_PROGRESS_BG, (bar_x, bar_y, 30, 4))
        pygame.draw.rect(screen, (0, 128, 255),        (bar_x, bar_y, int(30 * progress), 4))


def inject_pattern_for_stock(stock, pattern_key):
    try:
        stock.inject_named_pattern(pattern_key)
        return pattern_key
    except KeyError:
        return None


def draw_stock_summary(screen, font, stock, x, y):
    price_color = blue
    if stock.candles:
        price_color = green if stock.price >= stock.candles[-1].close else red
    screen.blit(font.render(f"Price: ${stock.price:.2f}", True, price_color), (x, y))
    screen.blit(font.render(f"Candles: {len(stock.candles)}", True, black), (x, y + 20))
    if stock.current_pattern_name:
        screen.blit(font.render(
            f"Pattern: {stock.current_pattern_name.replace('_', ' ').title()}",
            True, (0, 100, 200)), (x, y + 40))


def run(game):
    # 1. Shut down any default mixer allocations first
    if pygame.mixer.get_init():
        pygame.mixer.quit()

    # 2. Pre-init before pygame.init() — this is the only correct order
    pygame.mixer.pre_init(
        frequency=44100,
        size=-16,
        channels=2,
        buffer=4096
    )

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)

    display_info = pygame.display.Info()
    screen       = pygame.display.set_mode(
        (display_info.current_w, display_info.current_h), pygame.FULLSCREEN
    )
    SCREEN_W, SCREEN_H = display_info.current_w, display_info.current_h

    game_surface = pygame.Surface((GAME_W, GAME_H))
    assets       = load_all_assets()
    clock        = pygame.time.Clock()
    player       = game.players[0]
    game_clock   = GameClock()
    dt           = 16

    # ==========================================
    # AUDIO INIT
    # ==========================================
    sounds = load_sounds()
    music_play_bgm()

    # Track news state to trigger music switch only on change, not every frame
    last_news_state = False

    last_hovered        = None
    last_hover_sound_ms = 0

    # ==========================================
    # INITIAL GAME STATE
    # ==========================================
    state         = "menu"
    running       = True
    selected_char = 0
    anim_frame    = 0
    ticker_offset = 0

    market_open = False
    shop_open   = False

    buy_buttons        = []
    tab_buttons        = []
    selected_stock_idx = 0
    market_arrow_left  = market_arrow_right = pygame.Rect(0, 0, 0, 0)

    shop_tab       = "Desks"
    shop_scroll_y  = 0
    owned_items    = ["desk1", "wall1"]
    shop_close_btn = pygame.Rect(0, 0, 0, 0)

    confirm_open = False
    pending_item = None

    pattern_keys          = list(_ALL_PATTERNS.keys())
    PATTERN_INJECT_CHANCE = 0.20

    last_update       = pygame.time.get_ticks()
    stock_prev_prices = {s.name: s.price for s in game.stocks}

    # ==========================================
    # NEWS
    # ==========================================
    news               = News()
    news_open          = False
    selected_news_item = None

    news_btn_rect = pygame.Rect(GAME_W - 130, 50, 130, 45)
    back_btn      = pygame.Rect(0, 0, 0, 0)
    close_btn     = pygame.Rect(0, 0, 0, 0)
    card_rects    = []

    # ==========================================
    # DYNAMIC RENDER RECTS
    # ==========================================
    s_btn = c_btn = q_btn = pygame.Rect(0, 0, 0, 0)
    cards, b_btn, ok_btn  = [], pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
    menu_btn_rect         = pygame.Rect(GAME_W - 150, 15, 130, 45)
    yes_btn = no_btn      = pygame.Rect(0, 0, 0, 0)

    # ==========================================
    # MAIN LOOP
    # ==========================================
    while running:
        now = pygame.time.get_ticks()

        # ── Music: switch only when news state changes ──────────────
        # loops=-1 handles looping natively; no emergency recovery block needed.
        if news_open != last_news_state:
            if news_open:
                music_play_news()
            else:
                music_play_bgm()
            last_news_state = news_open

        # ── Mouse scaling ───────────────────────────────────────────
        raw_mouse  = pygame.mouse.get_pos()
        game_mouse = (
            raw_mouse[0] * GAME_W // SCREEN_W,
            raw_mouse[1] * GAME_H // SCREEN_H,
        )

        # Build list of hittable rects for hover sound
        hoverable = []
        if state == "menu":
            hoverable += [s_btn, c_btn, q_btn]
        elif state == "game":
            hoverable += [menu_btn_rect, news_btn_rect]
            if confirm_open:
                hoverable += [yes_btn, no_btn]
            elif news_open:
                if selected_news_item:
                    hoverable.append(close_btn)
                else:
                    hoverable.append(back_btn)
                    hoverable += [r for r, _ in card_rects if r and r.size != (0, 0)]
            elif shop_open:
                hoverable += [btn[0] for btn in buy_buttons if btn[0].size != (0, 0)]
                hoverable += [t["rect"] for t in tab_buttons if t["rect"].size != (0, 0)]
                hoverable.append(shop_close_btn)
            elif market_open:
                hoverable += [market_arrow_left, market_arrow_right]

        currently_hovered = next((r for r in hoverable if r.collidepoint(game_mouse)), None)

        if currently_hovered != last_hovered and currently_hovered is not None:
            if now - last_hover_sound_ms > 150:
                play(sounds, "hover")
                last_hover_sound_ms = now
        last_hovered = currently_hovered

        # ── Events ─────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEWHEEL and news_open and not selected_news_item:
                news.scroll(-event.y * 30)

            elif event.type == pygame.MOUSEWHEEL and shop_open and not confirm_open:
                shop_scroll_y += event.y * 30

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE) and state != "game":
                    if state == "char_select":
                        state = "menu"
                    else:
                        running = False

                elif state == "menu" and event.key == pygame.K_RETURN:
                    play(sounds, "click")
                    state = "game"

                elif state == "char_select":
                    if event.key == pygame.K_RETURN:
                        play(sounds, "click")
                        state = "menu"
                    elif event.key == pygame.K_LEFT:
                        selected_char = (selected_char - 1) % len(CHARACTERS)
                    elif event.key == pygame.K_RIGHT:
                        selected_char = (selected_char + 1) % len(CHARACTERS)

                elif state == "game":
                    if event.key == pygame.K_ESCAPE:
                        if confirm_open:
                            confirm_open = False
                        elif selected_news_item:
                            selected_news_item = None
                        elif news_open:
                            news_open = False
                        else:
                            state       = "menu"
                            market_open = False
                            shop_open   = False

                    elif event.key == pygame.K_q and market_open:
                        market_open = False

                    elif market_open and event.key == pygame.K_LEFT:
                        selected_stock_idx = (selected_stock_idx - 1) % len(game.stocks)
                    elif market_open and event.key == pygame.K_RIGHT:
                        selected_stock_idx = (selected_stock_idx + 1) % len(game.stocks)

                    elif event.key == pygame.K_TAB and not confirm_open:
                        shop_open   = not shop_open
                        market_open = False
                        news_open   = False

                    elif event.key == pygame.K_e and not market_open and not shop_open and not news_open:
                        p_rect = pygame.Rect(player.x, player.y, 64, 64)
                        if p_rect.colliderect(assets["computer_rect"].inflate(100, 100)):
                            play(sounds, "click")
                            market_open = True

                    elif event.key == pygame.K_n and not confirm_open:
                        play(sounds, "click")
                        news_open = not news_open
                        if news_open:
                            market_open = False
                            shop_open   = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gpt = mouse_clicked_in_game(event)
                clicked_valid_button = False

                if state == "menu":
                    if s_btn.collidepoint(gpt) or c_btn.collidepoint(gpt) or q_btn.collidepoint(gpt):
                        clicked_valid_button = True
                    if s_btn.collidepoint(gpt):
                        state = "game"
                    elif c_btn.collidepoint(gpt):
                        state = "char_select"
                    elif q_btn.collidepoint(gpt):
                        running = False

                elif state == "char_select":
                    if any(r.collidepoint(gpt) for r in cards) or b_btn.collidepoint(gpt) or ok_btn.collidepoint(gpt):
                        clicked_valid_button = True
                    for i, r in enumerate(cards):
                        if r.collidepoint(gpt):
                            selected_char = i
                    if b_btn.collidepoint(gpt) or ok_btn.collidepoint(gpt):
                        state = "menu"

                elif state == "game":
                    if menu_btn_rect.collidepoint(gpt) or news_btn_rect.collidepoint(gpt):
                        clicked_valid_button = True

                    if confirm_open:
                        if yes_btn.collidepoint(gpt) or no_btn.collidepoint(gpt):
                            clicked_valid_button = True
                        if yes_btn.collidepoint(gpt):
                            if player.cash >= pending_item["price"]:
                                play(sounds, "buy")
                                player.cash -= pending_item["price"]
                                owned_items.append(pending_item["id"])
                                cat = pending_item.get("category", "Desks")
                                if cat == "Desks":
                                    assets["current_desk_id"] = pending_item["id"]
                                elif cat == "Walls":
                                    assets["current_wall_id"] = pending_item["id"]
                                    if pending_item["id"] in assets["wall_masks"]:
                                        assets["walls_mask"] = assets["wall_masks"][pending_item["id"]]
                            confirm_open = False
                        elif no_btn.collidepoint(gpt):
                            confirm_open = False

                    else:
                        if menu_btn_rect.collidepoint(gpt):
                            state       = "menu"
                            market_open = False
                            shop_open   = False
                            news_open   = False

                        if market_open:
                            if market_arrow_left.collidepoint(gpt) or market_arrow_right.collidepoint(gpt):
                                clicked_valid_button = True
                            if market_arrow_left.collidepoint(gpt):
                                selected_stock_idx = (selected_stock_idx - 1) % len(game.stocks)
                            elif market_arrow_right.collidepoint(gpt):
                                selected_stock_idx = (selected_stock_idx + 1) % len(game.stocks)

                        elif shop_open:
                            if shop_close_btn.collidepoint(gpt) or any(t["rect"].collidepoint(gpt) for t in tab_buttons) or any(b[0].collidepoint(gpt) for b in buy_buttons):
                                clicked_valid_button = True
                            if shop_close_btn.collidepoint(gpt):
                                shop_open = False
                            for tab in tab_buttons:
                                if tab["rect"].collidepoint(gpt):
                                    shop_tab      = tab["category"]
                                    shop_scroll_y = 0
                            for btn_rect, item, btn_text in buy_buttons:
                                if btn_rect.collidepoint(gpt):
                                    if btn_text == "Buy" and player.cash >= item["price"]:
                                        confirm_open = True
                                        pending_item = item
                                    elif btn_text == "Equip":
                                        cat = item.get("category", "Desks")
                                        if cat == "Desks":
                                            assets["current_desk_id"] = item["id"]
                                        elif cat == "Walls":
                                            assets["current_wall_id"] = item["id"]
                                            if item["id"] in assets["wall_masks"]:
                                                assets["walls_mask"] = assets["wall_masks"][item["id"]]

                        elif news_btn_rect.collidepoint(gpt):
                            news_open = not news_open
                            if news_open:
                                shop_open   = False
                                market_open = False

                        if news_open:
                            if selected_news_item:
                                if close_btn.collidepoint(gpt):
                                    clicked_valid_button = True
                                    selected_news_item = None
                            else:
                                if back_btn.collidepoint(gpt) or any(cr.collidepoint(gpt) for cr, _ in card_rects if cr):
                                    clicked_valid_button = True
                                if back_btn.collidepoint(gpt):
                                    news_open = False
                                for card_rect, item in card_rects:
                                    if card_rect and card_rect.collidepoint(gpt):
                                        selected_news_item = item
                                        break

                if clicked_valid_button:
                    play(sounds, "click")

        # ── Render ──────────────────────────────────────────────────
        game_surface.fill(DARK)

        if state == "menu":
            s_btn, c_btn, q_btn = draw_menu(
                game_surface,
                assets["title_font"], assets["body_font"], assets["small_font"],
                assets["icon_play"],  assets["icon_person"], assets["icon_quit"]
            )

        elif state == "char_select":
            cards, b_btn, ok_btn = draw_char_select(
                game_surface,
                assets["title_font"], assets["body_font"], assets["small_font"],
                selected_char, assets["all_char_anims"], assets["char_images"]
            )

        elif state == "game":
            if now - last_update > 1000:
                stock_prev_prices = {s.name: s.price for s in game.stocks}
                game.update_stocks()
                last_update = now

            game_surface.blit(assets["bg"], (0, 0))

            for s in game.stocks:
                if not s.is_pattern_active() and random.random() < PATTERN_INJECT_CHANCE:
                    s.inject_named_pattern(random.choice(pattern_keys))

            current_wall_id = assets.get("current_wall_id")
            if current_wall_id in assets.get("wall_images", {}):
                game_surface.blit(assets["wall_images"][current_wall_id], (0, 0))

            current_desk = assets["desks"].get(assets["current_desk_id"])
            if current_desk:
                game_surface.blit(current_desk, assets["desk_rect"])

            for prop in MAP_PROPS:
                prop_img = assets["props"].get(prop["type"])
                if prop_img:
                    game_surface.blit(prop_img, (prop["x"], prop["y"]))

            menu_btn_rect = draw_top_bar(
                game_surface,
                assets["hud_font"], assets["small_font"], assets["hud_bold_font"],
                player, assets["icon_coin"], ticker_offset,
                game.stocks, stock_prev_prices
            )

            draw_button(game_surface, news_btn_rect, "📰 News", assets["small_font"], color=(40, 80, 120))

            ticker_offset -= 1.5
            if ticker_offset < -(len(game.stocks) * 180):
                ticker_offset = 0

            # Freeze world when UI overlays are open
            if not market_open and not shop_open and not confirm_open and not news_open:
                anim_frame = handle_player_movement(player, 3.5, anim_frame, assets)
                game_clock.update(dt)
                news.tick(game.stocks, game_clock)

            draw_clock_overlay(game_surface, assets["small_font"], assets["hud_font"], game_clock)

            p_rect = draw_player(
                game_surface, player, anim_frame,
                assets["all_char_anims"][selected_char],
                assets["char_images"][selected_char]
            )

            if p_rect.colliderect(assets["computer_rect"].inflate(100, 100)) and not market_open and not shop_open and not news_open:
                game_surface.blit(
                    assets["hud_font"].render("Press E to interact", True, GREEN),
                    (assets["computer_rect"].x - 20, assets["computer_rect"].y - 60)
                )

            if market_open:
                market_arrow_left, market_arrow_right = draw_market_overlay(
                    game_surface, assets["body_font"], assets["hud_font"],
                    assets["small_font"], game.stocks, selected_stock_idx
                )

            if shop_open:
                equipped_items = {
                    "Desks": assets.get("current_desk_id"),
                    "Walls": assets.get("current_wall_id"),
                }
                buy_buttons, tab_buttons, shop_scroll_y, shop_close_btn = draw_shop_overlay(
                    game_surface, assets["body_font"], assets["small_font"], player,
                    assets["icon_coin"], assets.get("shop_thumbnails", {}),
                    owned_items, equipped_items, shop_tab, shop_scroll_y
                )

            if confirm_open and pending_item:
                yes_btn, no_btn = draw_confirmation_screen(
                    game_surface, assets["body_font"], assets["small_font"],
                    f"Buy {pending_item['name']}?"
                )

            if news_open:
                back_btn, card_rects = draw_news_screen(
                    game_surface,
                    assets["title_font"], assets["body_font"], assets["small_font"],
                    news.news_items, news.scroll_offset, game_clock,
                )
                if selected_news_item:
                    close_btn = draw_news_detail(
                        game_surface,
                        assets["title_font"], assets["body_font"], assets["small_font"],
                        selected_news_item, game_clock,
                    )

        scaled = pygame.transform.scale(game_surface, (SCREEN_W, SCREEN_H))
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        dt = clock.tick(60)

    pygame.quit()
    sys.exit()