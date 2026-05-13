import pygame
import sys
import random

from .constants import *
from .screens import draw_menu, draw_char_select, draw_market_overlay, draw_shop_overlay, draw_confirmation_screen
from .assets.stock_assets import (
    CANDLE_COLORS, PATTERN_PROGRESS_BG, get_pattern_color, get_pattern_info
)
from .assets import stock_assets as pattern_assets
from features.interaction import mouse_clicked_in_game
from features.hud import draw_top_bar
from features.assets import load_all_assets
from features.player import handle_player_movement, draw_player
from game.stocks.patterns import PATTERNS as _ALL_PATTERNS

# Candlestick color aliases used by draw_candle / draw_stock_chart
light_green = CANDLE_COLORS["bullish"]["body"]
dark_green  = CANDLE_COLORS["bullish"]["border"]
light_red   = CANDLE_COLORS["bearish"]["body"]
dark_red    = CANDLE_COLORS["bearish"]["border"]

# General color aliases (lowercase) used throughout chart rendering
black      = (0, 0, 0)
gray       = (140, 140, 160)
light_gray = (240, 240, 240)
green      = (0, 200, 100)
red        = (255, 0, 0)
blue       = (50, 130, 255)

# Chart settings
CHART_WIDTH = 400
CHART_HEIGHT = 150
CHART_PADDING = 10
CANDLE_WIDTH = 10
CANDLE_SPACING = 4


def draw_candle(screen, x, y, ohlc, height_scale, min_price, max_price):
    open_p, high, low, close = ohlc
    chart_top = y + CHART_PADDING

    def price_to_y(price):
        return chart_top + (max_price - price) * height_scale

    open_y = price_to_y(open_p)
    close_y = price_to_y(close)
    high_y = price_to_y(high)
    low_y = price_to_y(low)

    if close >= open_p:
        color = light_green
        border_color = dark_green
        body_top = min(open_y, close_y)
        body_height = abs(close_y - open_y)
    else:
        color = light_red
        border_color = dark_red
        body_top = min(open_y, close_y)
        body_height = abs(close_y - open_y)

    pygame.draw.line(screen, black, (x, high_y), (x, low_y), 1)

    body_rect = pygame.Rect(x - CANDLE_WIDTH // 2, body_top, CANDLE_WIDTH, max(1, body_height))
    pygame.draw.rect(screen, color, body_rect)
    pygame.draw.rect(screen, border_color, body_rect, 1)


def draw_stock_chart(screen, font, stock, chart_x, chart_y, visible_candles=50):
    candles = stock.candles
    if not candles:
        return

    visible_candles_list = candles[-visible_candles:]
    if not visible_candles_list:
        return

    min_price = min(c.low for c in visible_candles_list)
    max_price = max(c.high for c in visible_candles_list)
    price_range = max_price - min_price
    if price_range == 0:
        price_range = 1

    chart_available_height = CHART_HEIGHT - 2 * CHART_PADDING
    height_scale = chart_available_height / price_range

    chart_rect = pygame.Rect(chart_x, chart_y, CHART_WIDTH, CHART_HEIGHT)
    pygame.draw.rect(screen, light_gray, chart_rect)
    pygame.draw.rect(screen, black, chart_rect, 1)

    grid_y = chart_y + CHART_PADDING
    grid_height = CHART_HEIGHT - 2 * CHART_PADDING
    num_grid_lines = 5
    for i in range(num_grid_lines + 1):
        y_pos = grid_y + (grid_height * i // num_grid_lines)
        pygame.draw.line(screen, gray, (chart_x, y_pos), (chart_x + CHART_WIDTH, y_pos), 1)

    total_candle_width = CANDLE_WIDTH + CANDLE_SPACING
    max_candles_fit = CHART_WIDTH // total_candle_width

    candle_x = chart_x + CHART_PADDING
    for candle in visible_candles_list:
        if candle_x + CANDLE_WIDTH > chart_x + CHART_WIDTH - CHART_PADDING:
            break

        draw_candle(
            screen, candle_x, chart_y,
            (candle.open, candle.high, candle.low, candle.close),
            height_scale, min_price, max_price
        )
        candle_x += total_candle_width

    price_y = chart_y + CHART_PADDING
    for i in range(num_grid_lines + 1):
        price_pos = max_price - (price_range * i // num_grid_lines)
        price_text = f"${price_pos:.1f}"
        text_surface = font.render(price_text, True, black)
        screen.blit(text_surface, (chart_x - 50, price_y - 5 + (grid_height * i // num_grid_lines)))


def draw_pattern_info(screen, font, stock, x, y):
    if stock.current_pattern_name is None: return

    pattern_name = stock.current_pattern_name
    pattern_info = pattern_assets.get_pattern_info(pattern_name)
    if pattern_info is None: return

    display_name, category, color_category = pattern_info
    color = pattern_assets.get_pattern_color(pattern_name)

    title_text = f"PATTERN: {display_name}"
    title_surface = font.render(title_text, True, color)
    screen.blit(title_surface, (x, y))

    category_text = f"CATEGORY: {category}"
    category_surface = font.render(category_text, True, (100, 100, 100))
    screen.blit(category_surface, (x, y + 20))

    if stock._active_segment:
        remaining_ticks, _ = stock._active_segment
        total_pattern_ticks = getattr(stock, '_pattern_total_ticks', 20)
        queue_ticks = sum(q[0] for q in stock._pattern_queue)
        
        completed = max(0, total_pattern_ticks - (queue_ticks + remaining_ticks))
        progress_pct = completed / total_pattern_ticks if total_pattern_ticks > 0 else 0

        bar_width, bar_height = 200, 12
        bar_x, bar_y = x, y + 45

        pygame.draw.rect(screen, PATTERN_PROGRESS_BG, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height), 1)
        pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_width * progress_pct), bar_height))

        num_indicators = min(10, total_pattern_ticks)
        indicator_spacing = bar_width // num_indicators
        for i in range(num_indicators):
            indicator_x = bar_x + (i * indicator_spacing) + indicator_spacing // 2
            pygame.draw.line(screen, gray, (indicator_x, bar_y - 3), (indicator_x, bar_y + bar_height + 3), 1)

        pct_surface = font.render(f"{int(progress_pct * 100)}%", True, black)
        screen.blit(pct_surface, (bar_x + bar_width + 10, bar_y))


def draw_candle_progress(screen, stock, x, y, candle_width=8, spacing=3):
    if not stock.candles and stock._current_candle is None: return
    current = stock._current_candle
    if current is None: return

    candle_base_y, candle_base_x = y + 10, x
    body_height, body_width = 20, candle_width

    ticks_per_candle = 5 
    progress = min(current.tick / ticks_per_candle, 1.0) if ticks_per_candle > 0 else 1.0
    alpha = int(255 * progress)

    if current.is_bullish(): body_color = (0, min(255, 150 + 100 * progress), 0, alpha)
    elif current.is_bearish(): body_color = (min(255, 200 + 55 * progress), 0, 0, alpha)
    else: body_color = (128, 128, 128, alpha)

    body_rect = pygame.Rect(candle_base_x, candle_base_y - body_height, body_width, body_height)
    pygame.draw.rect(screen, body_color[:3], body_rect)
    pygame.draw.rect(screen, black, body_rect, 1)

    if progress < 1.0:
        bar_x, bar_y = candle_base_x + body_width + 5, candle_base_y - body_height // 2
        pygame.draw.rect(screen, PATTERN_PROGRESS_BG, (bar_x, bar_y, 30, 4))
        pygame.draw.rect(screen, (0, 128, 255), (bar_x, bar_y, int(30 * progress), 4))


def inject_pattern_for_stock(stock, pattern_key):
    try:
        stock.inject_named_pattern(pattern_key)
        return pattern_key
    except KeyError:
        return None


def draw_stock_summary(screen, font, stock, x, y):
    price_text = f"Price: ${stock.price:.2f}"
    price_color = blue
    if stock.candles:
        last_close = stock.candles[-1].close
        price_color = green if stock.price >= last_close else red
    else:
        price_color = blue
    price_surface = font.render(price_text, True, price_color)
    screen.blit(price_surface, (x, y))

    # Candle count
    candle_count = len(stock.candles)
    candle_text = f"Candles: {candle_count}"
    candle_surface = font.render(candle_text, True, black)
    screen.blit(candle_surface, (x, y + 20))

    if stock.current_pattern_name:
        pattern_text = f"Pattern: {stock.current_pattern_name.replace('_', ' ').title()}"
        screen.blit(font.render(pattern_text, True, (0, 100, 200)), (x, y + 40))


def run(game):
    pygame.init()
    display_info = pygame.display.Info()
    screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
    SCREEN_W, SCREEN_H = display_info.current_w, display_info.current_h
    game_surface = pygame.Surface((GAME_W, GAME_H))

    assets = load_all_assets()
    clock = pygame.time.Clock()
    player = game.players[0]
    
    state = "menu"
    running = True

    selected_char = 0
    anim_frame = 0
    ticker_offset = 0
    
    market_open = False
    shop_open = False
    buy_buttons = []
    tab_buttons = []
    selected_stock_idx = 0
    market_arrow_left = market_arrow_right = pygame.Rect(0,0,0,0)
    
    shop_tab = "Desks"
    shop_scroll_y = 0
    owned_items = ["desk1", "wall1"]
    shop_close_btn = pygame.Rect(0,0,0,0)

    confirm_open = False
    pending_item = None

    # Pattern injection tracking
    pattern_keys = list(_ALL_PATTERNS.keys())
    PATTERN_INJECT_CHANCE = 0.20  # 20% chance per stock per tick
    
    last_update = pygame.time.get_ticks()
    stock_prev_prices = {stock.name: stock.price for stock in game.stocks}
    
    s_btn = c_btn = q_btn = pygame.Rect(0,0,0,0)
    cards, b_btn, ok_btn = [], pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0)
    menu_btn_rect = pygame.Rect(GAME_W - 150, 15, 130, 45)
    yes_btn = no_btn = pygame.Rect(0,0,0,0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
            elif event.type == pygame.MOUSEWHEEL and shop_open and not confirm_open:
                shop_scroll_y += event.y * 30
            
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
                    if event.key == pygame.K_ESCAPE: 
                        if confirm_open: confirm_open = False 
                        else:
                            state = "menu"
                            market_open = False
                            shop_open = False
                    elif event.key == pygame.K_q and market_open: 
                        market_open = False
                    elif market_open and event.key == pygame.K_LEFT:
                        selected_stock_idx = (selected_stock_idx - 1) % len(game.stocks)
                    elif market_open and event.key == pygame.K_RIGHT:
                        selected_stock_idx = (selected_stock_idx + 1) % len(game.stocks)
                    elif event.key == pygame.K_TAB and not confirm_open:  
                        shop_open = not shop_open
                        market_open = False
                    elif event.key == pygame.K_e and not market_open and not shop_open:
                        p_rect = pygame.Rect(player.x, player.y, 64, 64)
                        if p_rect.colliderect(assets["computer_rect"].inflate(100, 100)):
                            market_open = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gpt = mouse_clicked_in_game(event)
                
                if state == "menu":
                    if s_btn.collidepoint(gpt): state = "game"
                    elif c_btn.collidepoint(gpt): state = "char_select"
                    elif q_btn.collidepoint(gpt): running = False
                elif state == "char_select":
                    for i, r in enumerate(cards):
                        if r.collidepoint(gpt): selected_char = i
                    if b_btn.collidepoint(gpt) or ok_btn.collidepoint(gpt): state = "menu"
                elif state == "game":
                   
                    if confirm_open:
                        if yes_btn.collidepoint(gpt):
                            if player.cash >= pending_item["price"]:
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
                            state = "menu"
                            market_open = False
                            shop_open = False
                            
                        if market_open:
                            if market_arrow_left.collidepoint(gpt):
                                selected_stock_idx = (selected_stock_idx - 1) % len(game.stocks)
                            elif market_arrow_right.collidepoint(gpt):
                                selected_stock_idx = (selected_stock_idx + 1) % len(game.stocks)

                        if shop_open:
                            if shop_close_btn.collidepoint(gpt):
                                shop_open = False
                            for tab in tab_buttons:
                                if tab["rect"].collidepoint(gpt):
                                    shop_tab = tab["category"]
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

        game_surface.fill(DARK)

        if state == "menu":
            s_btn, c_btn, q_btn = draw_menu(
                game_surface, assets["title_font"], assets["body_font"], assets["small_font"], 
                assets["icon_play"], assets["icon_person"], assets["icon_quit"]
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
                last_update = pygame.time.get_ticks()

                # Randomly inject candlestick patterns
                for stock in game.stocks:
                    if not stock.is_pattern_active() and random.random() < PATTERN_INJECT_CHANCE:
                        pattern_key = random.choice(pattern_keys)
                        stock.inject_named_pattern(pattern_key)

            game_surface.blit(assets["bg"], (0, 0))
            
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
                game_surface, assets["hud_font"], assets["small_font"], player, 
                assets["icon_coin"], ticker_offset, game.stocks, stock_prev_prices
            )
            ticker_offset -= 1.5
            if ticker_offset < -(len(game.stocks) * 180): ticker_offset = 0
            
            if not market_open and not shop_open and not confirm_open:
                anim_frame = handle_player_movement(player, 3.5, anim_frame, assets)
                
            p_rect = draw_player(
                game_surface, player, anim_frame, 
                assets["all_char_anims"][selected_char], assets["char_images"][selected_char]
            )

            if p_rect.colliderect(assets["computer_rect"].inflate(100, 100)) and not market_open and not shop_open:
                game_surface.blit(assets["hud_font"].render("Press E to interact", True, GREEN), (assets["computer_rect"].x - 20, assets["computer_rect"].y - 60))

            if market_open:
                market_arrow_left, market_arrow_right = draw_market_overlay(
                    game_surface, assets["body_font"], assets["hud_font"],
                    assets["small_font"], game.stocks, selected_stock_idx
                )
                
            if shop_open:
                equipped_items = {
                    "Desks": assets.get("current_desk_id"),
                    "Walls": assets.get("current_wall_id")
                }
                buy_buttons, tab_buttons, shop_scroll_y, shop_close_btn = draw_shop_overlay(
                    game_surface, assets["body_font"], assets["small_font"], player, 
                    assets["icon_coin"], assets.get("shop_thumbnails", {}), owned_items, equipped_items, shop_tab, shop_scroll_y
                )
                                  
            if confirm_open and pending_item:
                yes_btn, no_btn = draw_confirmation_screen(
                    game_surface, assets["body_font"], assets["small_font"], 
                    f"Buy {pending_item['name']}?"
                )

        scaled = pygame.transform.scale(game_surface, (SCREEN_W, SCREEN_H))
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()