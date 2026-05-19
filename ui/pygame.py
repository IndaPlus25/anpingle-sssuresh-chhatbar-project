import pygame
import sys
import random
import os

from .constants import *
from .screens import (
    draw_menu, draw_day_night_cycle, draw_char_select, draw_market_overlay, 
    draw_shop_overlay, draw_confirmation_screen, draw_news_screen, draw_news_detail, 
    draw_staff_panel_overlay, draw_accounts_screen, draw_interaction_prompt, 
    draw_settings_overlay, open_settings, close_settings, is_settings_open, 
    get_music_volume, get_sfx_volume, apply_brightness_overlay, handle_settings_click,
    draw_portfolio_screen
)
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
from features.npc import EmployeeNPC
from features.placement import check_placement_valid, draw_placement_preview
from features.irs import IRSAgent, draw_audit_warning

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
# AUDIO STATE TRACKING (Fixed Addresses Folder Structure)
# ==========================================
MUSIC_BGM  = "ui/assets/music/prettyjohn1-corporate-background-music_33sec-483404.wav"
MUSIC_NEWS = "ui/assets/music/sonican-news-music-information-epic-30-seconds-471012.wav"
SFX_HOVER  = "ui/assets/music/finntastico-old-computer-click-152513.wav"
SFX_CLICK  = "ui/assets/music/freesoundeffects-button-click-289742 (1).wav"
SFX_BUY    = "ui/assets/music/freesound_community-cash-register-purchase-87313.wav"

_CURRENTLY_PLAYING_TRACK = None

def load_sounds():
    """Load sfx into a dict. Missing files are skipped gracefully."""
    sounds = {}
    sfx_files = {"hover": SFX_HOVER, "click": SFX_CLICK, "buy": SFX_BUY}
    for name, path in sfx_files.items():
        if os.path.exists(path):
            try: sounds[name] = pygame.mixer.Sound(path)
            except Exception as e: print(f"[Audio] Could not load {path}: {e}")
        else: print(f"[Audio] Missing sfx: {path}")

    if "hover" in sounds: sounds["hover"].set_volume(0.15)
    if "click" in sounds: sounds["click"].set_volume(0.4)
    if "buy"   in sounds: sounds["buy"].set_volume(0.6)
    return sounds

def play(sounds, name):
    if name in sounds: sounds[name].play()

def switch_music(track_name, filepath, volume=0.3):
    global _CURRENTLY_PLAYING_TRACK
    if _CURRENTLY_PLAYING_TRACK == track_name: 
        # Keep volume dynamic even if track doesn't switch
        pygame.mixer.music.set_volume(volume)
        return
    if not os.path.exists(filepath):
        print(f"[Audio] Missing music file at target: {filepath}")
        return

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=-1)
        _CURRENTLY_PLAYING_TRACK = track_name
    except Exception as e:
        print(f"[Audio] Music error ({track_name}): {e}")
        _CURRENTLY_PLAYING_TRACK = None

# --- RESTORED DYNAMIC VOLUME LINK TO TRACK MIXERS ---
def music_play_bgm(): switch_music("bgm", MUSIC_BGM, get_music_volume())
def music_play_news(): switch_music("news", MUSIC_NEWS, get_music_volume())

def draw_candle(screen, x, y, ohlc, height_scale, min_price, max_price):
    open_p, high, low, close = ohlc
    chart_top = y + CHART_PADDING
    def price_to_y(price): return chart_top + (max_price - price) * height_scale

    open_y, close_y = price_to_y(open_p), price_to_y(close)
    high_y, low_y   = price_to_y(high), price_to_y(low)

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
    if not candles: return
    visible_candles_list = candles[-visible_candles:]
    if not visible_candles_list: return

    min_price   = min(c.low  for c in visible_candles_list)
    max_price   = max(c.high for c in visible_candles_list)
    price_range = max_price - min_price or 1

    chart_available_height = CHART_HEIGHT - 2 * CHART_PADDING
    height_scale = chart_available_height / price_range

    chart_rect = pygame.Rect(chart_x, chart_y, CHART_WIDTH, CHART_HEIGHT)
    pygame.draw.rect(screen, light_gray, chart_rect)
    pygame.draw.rect(screen, black, chart_rect, 1)

    total_candle_width = CANDLE_WIDTH + CANDLE_SPACING
    candle_x           = chart_x + CHART_PADDING

    for candle in visible_candles_list:
        if candle_x + CANDLE_WIDTH > chart_x + CHART_WIDTH - CHART_PADDING: break
        draw_candle(screen, candle_x, chart_y, (candle.open, candle.high, candle.low, candle.close), height_scale, min_price, max_price)
        candle_x += total_candle_width

    price_y = chart_y + CHART_PADDING
    for i in range(6):
        price_pos = max_price - (price_range * i // 5)
        screen.blit(font.render(f"${price_pos:.1f}", True, black), (chart_x - 50, price_y - 5 + ((CHART_HEIGHT - 2 * CHART_PADDING) * i // 5)))

def draw_pattern_info(screen, font, stock, x, y):
    if stock.current_pattern_name is None: return
    pattern_name = stock.current_pattern_name
    pattern_info = pattern_assets.get_pattern_info(pattern_name)
    if pattern_info is None: return
    display_name, category, _ = pattern_info
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
        indicator_spacing = bar_width // min(10, total_pattern_ticks)
        for i in range(min(10, total_pattern_ticks)):
            indicator_x = bar_x + (i * indicator_spacing) + indicator_spacing // 2
            pygame.draw.line(screen, gray, (indicator_x, bar_y - 3), (indicator_x, bar_y + bar_height + 3), 1)
        screen.blit(font.render(f"{int(progress_pct * 100)}%", True, black), (bar_x + bar_width + 10, bar_y))

def draw_shadow_bubble(screen, stock, x, y, candle_width=8, spacing=3):
    if not stock.candles and stock._current_candle is None: return
    current = stock._current_candle
    if current is None: return
    candle_base_y, candle_base_x = y + 10, x
    body_height, body_width = 20, candle_width
    progress = min(current.tick / 5, 1.0)
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
    except KeyError: return None

def draw_stock_summary(screen, font, stock, x, y):
    price_color = blue
    if stock.candles: price_color = green if stock.price >= stock.candles[-1].close else red
    screen.blit(font.render(f"Price: ${stock.price:.2f}", True, price_color), (x, y))
    screen.blit(font.render(f"Candles: {len(stock.candles)}", True, black), (x, y + 20))
    if stock.current_pattern_name:
        screen.blit(font.render(f"Pattern: {stock.current_pattern_name.replace('_', ' ').title()}", True, (0, 100, 200)), (x, y + 40))


def run(game):
    if pygame.mixer.get_init(): pygame.mixer.quit()
    pygame.quit()
    
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
    pygame.init()
    
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)

    display_info = pygame.display.Info()
    screen       = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
    SCREEN_W, SCREEN_H = display_info.current_w, display_info.current_h

    game_surface = pygame.Surface((GAME_W, GAME_H))
    assets       = load_all_assets()
    clock        = pygame.time.Clock()
    player       = game.players[0]
    game_clock   = GameClock()
    dt           = 16

    sounds = load_sounds()
    music_play_bgm()

    last_news_state = False
    last_hovered        = None
    last_hover_sound_ms = 0
    
    player.offshore = 0
    player.owed_taxes = 0
    audit_active = False
    irs_agent = None
    wiring_funds = False
    post_audit_message = ""
    post_audit_timer = 0
    player.taxable_profit = 0  
    game_clock = GameClock()
    dt = 16 

    running = True

    # ==========================================
    # INITIAL GAME STATE
    # ==========================================
    state         = "menu"
    running       = True
    selected_char = 0
    anim_frame    = 0
    ticker_offset = 0

    market_open = False
    shop_open = False
    staff_open = False
    portfolio_open = False
    staff_buttons = []
    buy_buttons = []
    tab_buttons = []
    selected_stock_idx = 0
    market_arrow_left = market_arrow_right = market_close_btn = pygame.Rect(0,0,0,0)
    market_buy_btn = market_short_btn = market_amount_input = pygame.Rect(0,0,0,0)
    market_amount_text = ""
    market_input_active = False
    
    shop_tab = "Desks"
    shop_scroll_y = 0
    owned_items = ["desk1", "wall1"]
    shop_close_btn = pygame.Rect(0,0,0,0)
    staff_close_btn = pygame.Rect(0,0,0,0)

    confirm_open = False
    pending_item = None

    pattern_keys = list(_ALL_PATTERNS.keys())
    PATTERN_INJECT_CHANCE = 0.20  
    
    active_staff = {} 
    game_hour_timer = 0
    last_update = pygame.time.get_ticks()
    stock_prev_prices = {s.name: s.price for s in game.stocks}

    news               = News()
    news_open          = False
    selected_news_item = None

    news_btn_rect = pygame.Rect(GAME_W - 130, 50, 130, 45)
    back_btn      = pygame.Rect(0, 0, 0, 0)
    close_btn     = pygame.Rect(0, 0, 0, 0)
    card_rects    = []
    accounts_open = False
    accounts_close_btn = pygame.Rect(0,0,0,0)
    portfolio_close_btn = pygame.Rect(0,0,0,0)
    port_holdings_btn = pygame.Rect(0,0,0,0)
    port_history_btn = pygame.Rect(0,0,0,0)
    repatriate_btn = pygame.Rect(0,0,0,0)
    portfolio_scroll_y = 0
    portfolio_max_scroll = 0
    portfolio_tab = "Holdings"
    hours_until_audit = 168
    placement_mode = False
    placement_item_id = None
    placement_x, placement_y = 0, 0
    placed_props = []
    last_news_time = pygame.time.get_ticks()
    news_interval = random.randint(5000, 15000)

    s_btn = c_btn = settings_btn = q_btn = pygame.Rect(0, 0, 0, 0)
    cards, b_btn, ok_btn  = [], pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
    menu_btn_rect         = pygame.Rect(GAME_W - 150, 15, 130, 45)
    yes_btn = no_btn      = pygame.Rect(0, 0, 0, 0)
    
    settings_buttons = None

    while running:
        now = pygame.time.get_ticks()

        # Dynamic live evaluation sync triggers track volume changes safely context
        if news_open != last_news_state:
            if news_open: music_play_news()
            else: music_play_bgm()
            last_news_state = news_open

        raw_mouse  = pygame.mouse.get_pos()
        game_mouse = (raw_mouse[0] * GAME_W // SCREEN_W, raw_mouse[1] * GAME_H // SCREEN_H)

        hoverable = []
        if state == "menu":
            hoverable += [s_btn, c_btn, settings_btn, q_btn]
        elif state == "game" and not is_settings_open():
            hoverable += [menu_btn_rect, news_btn_rect]
            if confirm_open: hoverable += [yes_btn, no_btn]
            elif news_open:
                if selected_news_item: hoverable.append(close_btn)
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

        keys_pressed = pygame.key.get_pressed()
        
        if state == "game" and placement_mode and not is_settings_open():
            place_speed = 6
            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]: placement_x -= place_speed
            if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]: placement_x += place_speed
            if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]: placement_y -= place_speed
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]: placement_y += place_speed
            placement_x = max(0, min(GAME_W - 50, placement_x))
            placement_y = max(0, min(GAME_H - 50, placement_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEWHEEL and not is_settings_open():
                if news_open and not selected_news_item: news.scroll(-event.y * 30)
                elif shop_open and not confirm_open: shop_scroll_y += event.y * 30
                elif portfolio_open:
                    portfolio_scroll_y += event.y * 30 
                    portfolio_scroll_y = max(portfolio_max_scroll, min(0, portfolio_scroll_y))

            elif event.type == pygame.KEYDOWN:

                # =========================
                # IRS TEST TRIGGER (F12)
                # =========================
                if event.key == pygame.K_F12 and state == "game" and not audit_active:
                    if not hasattr(player, 'taxable_profit'): player.taxable_profit = 0
                    
                    if player.taxable_profit > 0:
                        audit_active = True
                        post_audit_message = ""
                        accountants = sum(1 for e in active_staff.values() if getattr(e, 'role', 'Salesman') == "Accountant" and e.energy > 0)
                        
                        # Save the tax rate and the starting profit for the audit
                        player.tax_rate = max(0.15 - (0.02 * accountants), 0.05)
                        player.audit_starting_profit = player.taxable_profit 
                        player.hidden_profit = 0
                        player.wire_progress = 0.0
                        
                        desk_x = assets["computer_rect"].x
                        desk_y = assets["computer_rect"].y
                        irs_agent = IRSAgent(GAME_W // 2, GAME_H + 50, desk_x, desk_y + 80)
                    else:
                        print("No capital gains to tax this week!")

                if event.key in (pygame.K_q, pygame.K_ESCAPE) and state != "game" and not is_settings_open():
                    if state == "char_select": state = "menu"
                    else: running = False

                elif state == "menu" and event.key == pygame.K_RETURN:
                    play(sounds, "click")
                    state = "game"

                elif state == "char_select":
                    if event.key == pygame.K_RETURN:
                        play(sounds, "click")
                        state = "menu"
                    elif event.key == pygame.K_LEFT: selected_char = (selected_char - 1) % len(CHARACTERS)
                    elif event.key == pygame.K_RIGHT: selected_char = (selected_char + 1) % len(CHARACTERS)

                elif state == "game":
                    if event.key == pygame.K_ESCAPE:
                        if is_settings_open(): close_settings()
                        elif placement_mode: placement_mode = False
                        elif confirm_open: confirm_open = False
                        elif selected_news_item: selected_news_item = None
                        elif news_open: news_open = False
                        elif accounts_open: accounts_open = False
                        elif portfolio_open: portfolio_open = False
                        else: open_settings() 
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE) and placement_mode and not is_settings_open():
                        if check_placement_valid(placement_x, placement_y, placement_item_id, assets, placed_props):
                            placed_props.append({"id": placement_item_id, "x": placement_x, "y": placement_y})
                            if placement_item_id in owned_items: owned_items.remove(placement_item_id)
                            placement_mode = False
                    elif event.key == pygame.K_q and market_open and not is_settings_open(): market_open = False
                    elif market_open and event.key == pygame.K_LEFT and not is_settings_open(): selected_stock_idx = (selected_stock_idx - 1) % len(game.stocks)
                    elif market_open and event.key == pygame.K_RIGHT and not is_settings_open(): selected_stock_idx = (selected_stock_idx + 1) % len(game.stocks)
                    elif market_input_active and market_open and event.key == pygame.K_BACKSPACE and not is_settings_open(): market_amount_text = market_amount_text[:-1]
                    elif market_input_active and market_open and event.unicode.isdigit() and not is_settings_open():
                        if len(market_amount_text) < 10: market_amount_text += event.unicode
                    elif event.key == pygame.K_TAB and not confirm_open and not is_settings_open():  
                        shop_open = not shop_open
                        market_open = staff_open = news_open = accounts_open = portfolio_open = False
                    elif event.key == pygame.K_t and not confirm_open and not is_settings_open(): 
                        staff_open = not staff_open
                        market_open = shop_open = news_open = accounts_open = portfolio_open = False
                    elif event.key == pygame.K_b and not confirm_open and not is_settings_open():
                        accounts_open = not accounts_open
                        if accounts_open: market_open = shop_open = staff_open = news_open = portfolio_open = False
                    elif event.key == pygame.K_p and not confirm_open and not is_settings_open():
                        play(sounds, "click")
                        portfolio_open = not portfolio_open
                        if portfolio_open: market_open = shop_open = staff_open = news_open = accounts_open = False
                    elif event.key == pygame.K_e and not any([market_open, shop_open, news_open, staff_open, accounts_open, portfolio_open, is_settings_open()]):
                        if pygame.Rect(player.x, player.y, 64, 64).colliderect(assets["computer_rect"].inflate(100, 100)):
                            play(sounds, "click")
                            market_open = True
                    elif event.key == pygame.K_n and not confirm_open and not is_settings_open():
                        play(sounds, "click")
                        news_open = not news_open
                        if news_open: market_open = shop_open = accounts_open = portfolio_open = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gpt = mouse_clicked_in_game(event)
                
                if is_settings_open() and settings_buttons:
                    handle_settings_click(settings_buttons, game_mouse)
                    # Sync hardware runtime audio mixer settings instantly upon click capture context loop hook
                    if _CURRENTLY_PLAYING_TRACK == "news": music_play_news()
                    else: music_play_bgm()
                    for sound in sounds.values(): sound.set_volume(get_sfx_volume())
                    continue

                clicked_valid_button = False
                if state == "menu":
                    if s_btn.collidepoint(gpt): state = "game"
                    elif c_btn.collidepoint(gpt): state = "char_select"
                    elif settings_btn.collidepoint(gpt): open_settings()
                    elif q_btn.collidepoint(gpt): running = False

                elif state == "char_select":
                    if any(r.collidepoint(gpt) for r in cards) or b_btn.collidepoint(gpt) or ok_btn.collidepoint(gpt): clicked_valid_button = True
                    for i, r in enumerate(cards):
                        if r.collidepoint(gpt): selected_char = i
                    if b_btn.collidepoint(gpt) or ok_btn.collidepoint(gpt): state = "menu"

                elif state == "game":
                    if menu_btn_rect.collidepoint(gpt) or news_btn_rect.collidepoint(gpt): clicked_valid_button = True
                    if confirm_open:
                        if yes_btn.collidepoint(gpt) or no_btn.collidepoint(gpt): clicked_valid_button = True
                        if yes_btn.collidepoint(gpt):
                            if player.cash >= pending_item["price"]:
                                play(sounds, "buy")
                                player.cash -= pending_item["price"]
                                owned_items.append(pending_item["id"])
                                cat = pending_item.get("category", "Desks")
                                if cat == "Desks": assets["current_desk_id"] = pending_item["id"]
                                elif cat == "Walls":
                                    assets["current_wall_id"] = pending_item["id"]
                                    if pending_item["id"] in assets["wall_masks"]: assets["walls_mask"] = assets["wall_masks"][pending_item["id"]]
                            confirm_open = False
                        elif no_btn.collidepoint(gpt): confirm_open = False
                    else:
                        if menu_btn_rect.collidepoint(gpt):
                            state = "menu"
                            market_open = shop_open = staff_open = False
                        if portfolio_open:
                            if portfolio_close_btn.collidepoint(gpt):
                                clicked_valid_button = True
                                portfolio_open = False
                            if port_holdings_btn.collidepoint(gpt) and portfolio_tab != "Holdings":
                                clicked_valid_button = True
                                portfolio_tab = "Holdings"
                                portfolio_scroll_y = 0
                            if port_history_btn.collidepoint(gpt) and portfolio_tab != "History":
                                clicked_valid_button = True
                                portfolio_tab = "History"
                                portfolio_scroll_y = 0
                        if market_open:
                            if market_arrow_left.collidepoint(gpt) or market_arrow_right.collidepoint(gpt) or market_close_btn.collidepoint(gpt): clicked_valid_button = True
                            if market_close_btn.collidepoint(gpt): market_open = False
                            if market_arrow_left.collidepoint(gpt): selected_stock_idx = (selected_stock_idx - 1) % len(game.stocks)
                            elif market_arrow_right.collidepoint(gpt): selected_stock_idx = (selected_stock_idx + 1) % len(game.stocks)
                            market_input_active = True if market_amount_input.collidepoint(gpt) else False

                            current_stock = game.stocks[selected_stock_idx]
                            try:
                                amount = int(market_amount_text) if market_amount_text else 0
                            except ValueError:
                                amount = 0

                            if not hasattr(player, 'portfolio'): player.portfolio = {}

                            if market_amount_input.collidepoint(gpt):
                                market_input_active = True
                            else:
                                market_input_active = False

                            if market_buy_btn.collidepoint(gpt) and amount > 0:
                                total_cost = amount * current_stock.price
                                if player.buy_stock(current_stock.name, current_stock.price, amount):
                                    play(sounds, "buy")
                                    
                                    # Update cost basis for IRS logic
                                    if not hasattr(player, 'cost_basis'): player.cost_basis = {}
                                    old_shares = player.portfolio[current_stock.name] - amount
                                    old_avg = player.cost_basis.get(current_stock.name, current_stock.price)
                                    total_shares = player.portfolio[current_stock.name]
                                    new_avg = ((old_shares * old_avg) + (amount * current_stock.price)) / total_shares if total_shares > 0 else 0
                                    player.cost_basis[current_stock.name] = new_avg

                                    if not hasattr(player, 'trade_history'): player.trade_history = []
                                    player.trade_history.append({
                                        "action": "BUY", "ticker": current_stock.name,
                                        "shares": amount, "price": current_stock.price,
                                        "total": total_cost, "pnl": 0
                                    })
                                    market_amount_text = ""

                            if market_short_btn.collidepoint(gpt) and amount > 0:
                                play(sounds, "buy")
                                player.short_stock(current_stock.name, current_stock.price, amount)
                                if not hasattr(player, 'trade_history'): player.trade_history = []
                                player.trade_history.append({
                                    "action": "SHORT", "ticker": current_stock.name,
                                    "shares": amount, "price": current_stock.price,
                                    "total": amount * current_stock.price, "pnl": 0
                                })
                                market_amount_text = ""
                        elif shop_open:
                            if shop_close_btn.collidepoint(gpt) or any(t["rect"].collidepoint(gpt) for t in tab_buttons) or any(b[0].collidepoint(gpt) for b in buy_buttons): clicked_valid_button = True
                            if shop_close_btn.collidepoint(gpt): shop_open = False
                            for tab in tab_buttons:
                                if tab["rect"].collidepoint(gpt): shop_tab, shop_scroll_y = tab["category"], 0
                            for btn_rect, item, btn_text in buy_buttons:
                                if btn_rect.collidepoint(gpt):
                                    if btn_text == "Buy" and player.cash >= item["price"]: confirm_open, pending_item = True, item
                                    elif btn_text == "Equip":
                                        cat = item.get("category", "Desks")
                                        if cat == "Desks": assets["current_desk_id"] = item["id"]
                                        elif cat == "Walls":
                                            assets["current_wall_id"] = item["id"]
                                            if item["id"] in assets["wall_masks"]: assets["walls_mask"] = assets["wall_masks"][item["id"]]
                                    elif btn_text == "Place":
                                        placement_mode, placement_item_id = True, item["id"]
                                        placement_x, placement_y = player.x, player.y
                                        shop_open = False
                        if accounts_open:
                            if accounts_close_btn.collidepoint(gpt): accounts_open = False
                            elif repatriate_btn.collidepoint(gpt) and player.offshore > 0:
                                penalty = player.offshore * 0.10
                                repat_amount = player.offshore - penalty
                                

                                if not hasattr(player, 'trade_history'): player.trade_history = []
                                player.trade_history.append({
                                    "action": "REPAT", "ticker": "OFFSHORE",
                                    "shares": 0, "price": 0,
                                    "total": repat_amount, "pnl": repat_amount 
                                })
                                
                                player.cash += repat_amount
                                player.offshore = 0
                        if staff_open:
                            if staff_close_btn.collidepoint(gpt): staff_open = False
                            for btn in staff_buttons:
                                emp_id = btn["id"]
                                if btn["hire_rect"].collidepoint(gpt) and emp_id not in active_staff:
                                    active_staff[emp_id] = EmployeeNPC(random.randint(200, GAME_W - 200), random.randint(200, GAME_H - 200), btn["config"])
                                elif btn["fire_rect"].collidepoint(gpt) and emp_id in active_staff: del active_staff[emp_id]
                                elif "role_rect" in btn and btn["role_rect"].collidepoint(gpt) and emp_id in active_staff:
                                    npc = active_staff[emp_id]
                                    if npc.role == "Salesman":
                                        if sum(1 for e in active_staff.values() if getattr(e, 'role', 'Salesman') == "Accountant") < 3: npc.role = "Accountant"
                                    else: npc.role = "Salesman"
                        if news_btn_rect.collidepoint(gpt):
                            news_open = not news_open
                            if news_open: market_open = shop_open = accounts_open = portfolio_open = False
                        if news_open:
                            if selected_news_item:
                                if close_btn.collidepoint(gpt): clicked_valid_button, selected_news_item = True, None
                            else:
                                if back_btn.collidepoint(gpt) or any(cr.collidepoint(gpt) for cr, _ in card_rects if cr): clicked_valid_button = True
                                if back_btn.collidepoint(gpt): news_open = False
                                for card_rect, item in card_rects:
                                    if card_rect and card_rect.collidepoint(gpt): selected_news_item = item; break
                if clicked_valid_button: play(sounds, "click")

        # ── Frame Buffer Graphics Pass ──────────────────────────────
        game_surface.fill(DARK)

        if state == "menu":
            s_btn, c_btn, settings_btn, q_btn = draw_menu(
                game_surface, assets["title_font"], assets["body_font"], assets["small_font"],
                assets["icon_play"], assets["icon_person"], assets["icon_quit"], assets.get("icon_settings")
            )
        elif state == "char_select":
            cards, b_btn, ok_btn = draw_char_select(
                game_surface, assets["title_font"], assets["body_font"], assets["small_font"],
                selected_char, assets["all_char_anims"], assets["char_images"]
            )
        elif state == "game":
            if pygame.time.get_ticks() - last_update > 1000:
                stock_prev_prices = {stock.name: stock.price for stock in game.stocks}
                game.update_stocks()
                player.settle_shorts(game.stocks, stock_prev_prices)

                last_update = pygame.time.get_ticks()

            current_time = pygame.time.get_ticks()
            if current_time - last_news_time > news_interval:
                news.add_item(generate_random_story(game.stocks, game_clock))
                news.apply_to_stocks(game.stocks)
                last_news_time = current_time
                news_interval = random.randint(10000, 30000)

            game_surface.blit(assets["bg"], (0, 0))
            draw_button(game_surface, news_btn_rect, "News", assets["small_font"], color=(40, 80, 120))

            for stock in game.stocks:
                if not stock.is_pattern_active() and random.random() < PATTERN_INJECT_CHANCE:
                    stock.inject_named_pattern(random.choice(pattern_keys))
            
            if assets.get("current_wall_id") in assets.get("wall_images", {}):
                game_surface.blit(assets["wall_images"][assets["current_wall_id"]], (0, 0))
            if assets["desks"].get(assets["current_desk_id"]):
                game_surface.blit(assets["desks"].get(assets["current_desk_id"]), assets["desk_rect"])

            for prop in MAP_PROPS:
                if assets["props"].get(prop["type"]): game_surface.blit(assets["props"].get(prop["type"]), (prop["x"], prop["y"]))
            for p in placed_props:
                if assets.get("placeables", {}).get(p["id"]): game_surface.blit(assets["placeables"][p["id"]], (p["x"], p["y"]))
                    
            if placement_mode:
                is_valid = check_placement_valid(placement_x, placement_y, placement_item_id, assets, placed_props)
                draw_placement_preview(game_surface, placement_item_id, placement_x, placement_y, is_valid, assets)
                draw_interaction_prompt(game_surface, assets["small_font"], "WASD/Arrows to move | ENTER to place | ESC to cancel", GAME_W // 2, GAME_H - 20, border_color=(80, 200, 120) if is_valid else (255, 100, 100))

            p_rect = pygame.Rect(player.x, player.y, 64, 64)
            wiring_funds = False
            if audit_active and irs_agent.state == "approaching":
                if p_rect.colliderect(assets["computer_rect"].inflate(100, 100)):
                    # Check if there is still onshore profit to hide
                    if keys_pressed[pygame.K_SPACE] and player.taxable_profit > 0:
                        wiring_funds = True
                        
                        # Transfer 20% of your total profits per second
                        transfer_pct_per_sec = 0.15 
                        chunk = player.audit_starting_profit * transfer_pct_per_sec * (dt / 1000.0)
                        
                        chunk = min(chunk, player.taxable_profit) # Can't hide more than is left
                        chunk = min(chunk, player.cash)           # Can't hide money you don't have
                        
                        if chunk > 0:
                            player.cash -= chunk
                            player.offshore += chunk
                            
                            # Move the profit from "Taxable" to "Hidden"
                            player.taxable_profit -= chunk 
                            player.hidden_profit += chunk
                            
                            # Calculate the progress bar
                            player.wire_progress = player.hidden_profit / player.audit_starting_profit


            # =========================
            # TOP BAR
            # =========================
            menu_btn_rect = draw_top_bar(
                game_surface,
                assets["hud_font"], assets["small_font"], assets["hud_bold_font"],
                player, assets["icon_coin"], ticker_offset,
                game.stocks, stock_prev_prices
            )

            hm_x, hm_y = menu_btn_rect.right - 33, menu_btn_rect.y + 11
            pygame.draw.line(game_surface, (255, 255, 255), (hm_x, hm_y), (hm_x + 20, hm_y), 3)
            pygame.draw.line(game_surface, (255, 255, 255), (hm_x, hm_y + 7), (hm_x + 20, hm_y + 7), 3)
            pygame.draw.line(game_surface, (255, 255, 255), (hm_x, hm_y + 14), (hm_x + 20, hm_y + 14), 3)


            draw_button(game_surface, news_btn_rect, "News", assets["small_font"], color=(40, 80, 120))

            ticker_offset -= 1.5
            if ticker_offset < -(len(game.stocks) * 180): ticker_offset = 0
            assets["placed_props"] = placed_props

            if not any([placement_mode, market_open, shop_open, staff_open, accounts_open, portfolio_open, confirm_open, wiring_funds, is_settings_open()]):
                anim_frame = handle_player_movement(player, 3.5, anim_frame, assets)
                game_clock.update(dt)
                game_hour_timer += dt
                
                if game_hour_timer >= GAME_HOUR_MS:
                    game_hour_timer -= GAME_HOUR_MS
                    
                    if not hasattr(player, 'taxable_profit'): player.taxable_profit = 0
                    live_accountants = sum(1 for e in active_staff.values() if getattr(e, 'role', 'Salesman') == "Accountant" and e.energy > 0)
                    live_rate = max(0.35 - (0.03 * live_accountants), 0.05)
                    
                    player.pending_tax = player.taxable_profit * live_rate if player.taxable_profit > 0 else 0

                    is_night = game_clock.current_time.hour >= 18 or game_clock.current_time.hour < 6

                    total_salary_paid = 0
                    for emp_id, emp_npc in active_staff.items():
                        base_salary = emp_npc.config["salary"]

                        if is_night:
                            salary = int(base_salary * 2.5)
                            emp_npc.energy = max(0, emp_npc.energy - 10) 
                        else:
                            salary = base_salary

                        player.cash -= salary
                        total_salary_paid += salary
                        if getattr(emp_npc, 'role', 'Salesman') == "Salesman" and emp_npc.energy > 0:
                            player.cash += (base_salary * 2.0)

                    hours_until_audit -= 1
                    if hours_until_audit <= 0:
                        if not hasattr(player, 'taxable_profit'): player.taxable_profit = 0
                        
                        if player.taxable_profit > 0 and not audit_active:
                            audit_active = True
                            post_audit_message = ""
                            accountants = sum(1 for e in active_staff.values() if getattr(e, 'role', 'Salesman') == "Accountant" and e.energy > 0)
                            
                            # --- NEW: Save the starting state for the hide-the-money mini-game! ---
                            player.tax_rate = max(0.35 - (0.02 * accountants), 0.05)
                            player.audit_starting_profit = player.taxable_profit 
                            player.hidden_profit = 0
                            player.wire_progress = 0.0
                            
                            desk_x = assets["computer_rect"].x
                            desk_y = assets["computer_rect"].y
                            irs_agent = IRSAgent(GAME_W // 2, GAME_H + 50, desk_x, desk_y + 80)
                        else:
                            # If no profit was made, wipe the slate clean for next week anyway
                            player.taxable_profit = 0
                            
                        hours_until_audit = 168 # Reset timer for next week

                # Aligned perfectly to 4-spaces inside the if statement!
                for emp_id, emp_npc in active_staff.items(): 
                    emp_npc.update(dt, assets)
                
            for emp_id, emp_npc in active_staff.items():
                if emp_id in assets["staff_anims"]: emp_npc.draw(game_surface, assets["staff_anims"][emp_id], assets["small_font"])
                    
            draw_clock_overlay(game_surface, assets["small_font"], assets["hud_font"], game_clock)
            p_rect = draw_player(game_surface, player, anim_frame, assets["all_char_anims"][selected_char], assets["char_images"][selected_char])
            draw_day_night_cycle(game_surface, game_clock, player, assets.get("computer_rect"))
            # =========================
            # INTERACTION TEXT
            # =========================
            if not any([placement_mode, market_open, shop_open, accounts_open, news_open, staff_open, portfolio_open, confirm_open]):
                
                # Check if player is near the computer desk
                if p_rect.colliderect(assets["computer_rect"].inflate(100, 100)):
                    
                    # Position the prompt perfectly centered above the computer
                    prompt_x = assets["computer_rect"].centerx
                    prompt_y = assets["computer_rect"].top - 10
                    
                    if audit_active and irs_agent.state == "approaching":
                        if wiring_funds:
                            pct = int(player.wire_progress * 100)
                            draw_interaction_prompt(
                                game_surface, assets["small_font"], 
                                f"WIRING OFFSHORE: {pct}%", prompt_x, prompt_y,
                                border_color=(255, 100, 100)
                            )
                            
                            bar_w = 180
                            bar_h = 8
                            bar_x = prompt_x - (bar_w // 2)
                            bar_y = prompt_y + 18 # Placed right below the text box
                            
                            # Draw dark background
                            pygame.draw.rect(game_surface, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
                            # Draw green fill
                            fill_w = int(bar_w * player.wire_progress)
                            if fill_w > 0:
                                pygame.draw.rect(game_surface, (0, 200, 100), (bar_x, bar_y, fill_w, bar_h), border_radius=4)

                        else:
                            draw_interaction_prompt(
                                game_surface, assets["small_font"], 
                                "Hold SPACE to transfer money", prompt_x, prompt_y,
                                border_color=(255, 100, 100)
                            )
                    elif not audit_active:
                        draw_interaction_prompt(
                            game_surface, assets["small_font"], 
                            "Press E to Trade", prompt_x, prompt_y,
                            border_color=(80, 200, 120) 
                        )

            
            if audit_active:
                current_tax_bill = player.taxable_profit * player.tax_rate
                draw_audit_warning(game_surface, assets["hud_font"], current_tax_bill, GAME_W)
                reached_desk = irs_agent.update(dt, assets)
                irs_agent.draw(game_surface, assets["small_font"], assets.get("irs_anims"))
                
                if reached_desk:
                    if keys_pressed[pygame.K_SPACE]:
                        # --- CAUGHT! SEC SEIZES 100% OF THE TOTAL WEEKLY PROFIT ---
                        sec_fine = player.audit_starting_profit
                        
                        # They rip the hidden money back out of your offshore account
                        player.offshore = max(0, player.offshore - player.hidden_profit)
                        # They take the remaining unhidden profit from your cash
                        player.cash -= player.taxable_profit 
                        
                        if not hasattr(player, 'trade_history'): player.trade_history = []
                        if sec_fine > 0:
                            player.trade_history.append({
                                "action": "FINE", "ticker": "SEC", 
                                "shares": 0, "price": 0, 
                                "total": sec_fine, "pnl": -sec_fine 
                            })

                        total_left = player.cash + player.offshore
                        post_audit_message = f"CAUGHT! SEC SEIZED ${sec_fine:,.0f} | LEFT: ${total_left:,.0f}"
                        irs_agent.speech_text = "Fraud detected. Seizing all capital gains."
                        
                    else:
                        # --- SAFE! IRS ONLY TAXES WHATS LEFT ONSHORE ---
                        final_tax_bill = player.taxable_profit * player.tax_rate
                        player.cash -= final_tax_bill
                        
                        if not hasattr(player, 'trade_history'): player.trade_history = []
                        if final_tax_bill > 0:
                            player.trade_history.append({
                                "action": "TAX", "ticker": "IRS", 
                                "shares": 0, "price": 0, 
                                "total": final_tax_bill, "pnl": -final_tax_bill
                            })
                            
                        if player.hidden_profit > 0:
                            player.trade_history.append({
                                "action": "WIRE", "ticker": "OFFSHORE", 
                                "shares": 0, "price": 0, 
                                "total": player.hidden_profit, "pnl": -player.hidden_profit 
                            })

                        total_left = player.cash + player.offshore
                        post_audit_message = f"TAXED ${final_tax_bill:,.0f} | HIDDEN: ${player.hidden_profit:,.0f} | LEFT: ${total_left:,.0f}"
                        irs_agent.speech_text = f"Collected taxes. Have a nice day."
                        
                    # Reset the pools for next week
                    player.taxable_profit = 0 
                    player.hidden_profit = 0
                    
                    irs_agent.state = "leaving"
                    post_audit_timer = 4000
                    audit_active = False

            if post_audit_timer > 0:
                post_audit_timer -= dt
                msg_rect = pygame.Rect(GAME_W//2 - 300, GAME_H//2 - 50, 600, 100)
                pygame.draw.rect(game_surface, (20, 20, 20), msg_rect, border_radius=10)
                pygame.draw.rect(game_surface, (255, 215, 0), msg_rect, 3, border_radius=10)
                msg_surf = assets["small_font"].render(post_audit_message, True, (255, 215, 0))
                game_surface.blit(msg_surf, msg_surf.get_rect(center=msg_rect.center))
                irs_agent.update(dt, assets) 
                irs_agent.draw(game_surface, assets["small_font"], assets.get("irs_anims"))


            # =========================
            # UI OVERLAYS
            # =========================
            if market_open:
                market_arrow_left, market_arrow_right, market_buy_btn, market_short_btn, market_amount_input, market_close_btn = draw_market_overlay(
                    game_surface, assets["body_font"], assets["hud_font"],
                    assets["small_font"], game.stocks, selected_stock_idx,
                    player.cash, player.portfolio, player.shorts,
                    market_amount_text, market_input_active, ticker_offset
                )
                
            if staff_open:
                staff_buttons, staff_close_btn = draw_staff_panel_overlay(
                    game_surface, assets["body_font"], assets["small_font"], 
                    active_staff, AVAILABLE_EMPLOYEES, assets["staff_portraits"]
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
            

            if accounts_open:
                accounts_close_btn, repatriate_btn = draw_accounts_screen(
                    game_surface, assets["title_font"], assets["body_font"], assets["small_font"], player
                )
                                  
            if confirm_open and pending_item:
                yes_btn, no_btn = draw_confirmation_screen(
                    game_surface, assets["body_font"], assets["small_font"],
                    f"Buy {pending_item['name']}?"
                )

            if portfolio_open: 
                portfolio_close_btn, portfolio_max_scroll, port_holdings_btn, port_history_btn = draw_portfolio_screen(game_surface, assets["title_font"], assets["body_font"], assets["small_font"], player, game.stocks, portfolio_scroll_y, portfolio_tab)
            if news_open:
                back_btn, card_rects = draw_news_screen(game_surface, assets["title_font"], assets["body_font"], assets["small_font"], news.news_items, news.scroll_offset, game_clock)
                if selected_news_item: close_btn = draw_news_detail(game_surface, assets["title_font"], assets["body_font"], assets["small_font"], selected_news_item, game_clock)

        if is_settings_open():
            mouse_down = pygame.mouse.get_pressed()[0]
            settings_buttons = draw_settings_overlay(game_surface, assets["title_font"], assets["body_font"], assets["small_font"], game_mouse, mouse_down)

        apply_brightness_overlay(game_surface)
        screen.blit(pygame.transform.scale(game_surface, (SCREEN_W, SCREEN_H)), (0, 0))
        pygame.display.flip()
        dt = clock.tick(60)

    pygame.quit()
    sys.exit()