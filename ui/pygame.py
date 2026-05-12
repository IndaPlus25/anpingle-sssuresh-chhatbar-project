import pygame
import sys

from .constants import *
from .screens import draw_menu, draw_char_select, draw_market_overlay, draw_shop_overlay, draw_confirmation_screen
from features.interaction import mouse_clicked_in_game
from features.hud import draw_top_bar, draw_clock_overlay
from features.assets import load_all_assets
from features.player import handle_player_movement, draw_player
from features.clock import GameClock

# Chart settings
CHART_WIDTH = 400
CHART_HEIGHT = 150
CHART_PADDING = 10
CANDLE_WIDTH = 10
CANDLE_SPACING = 4


def draw_candle(screen, x, y, ohlc, height_scale, min_price, max_price):
    """Draw a single candlestick.

    ohlc: (open, high, low, close) prices
    height_scale: pixels per price unit
    min_price: minimum price for chart scaling
    max_price: maximum price for chart scaling
    """
    open_p, high, low, close = ohlc
    chart_top = y + CHART_PADDING

    # Calculate y positions (invert y for Pygame)
    def price_to_y(price):
        return chart_top + (max_price - price) * height_scale

    open_y = price_to_y(open_p)
    close_y = price_to_y(close)
    high_y = price_to_y(high)
    low_y = price_to_y(low)

    # Determine color
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

    # Draw wick
    pygame.draw.line(screen, black, (x, high_y), (x, low_y), 1)

    # Draw body
    body_rect = pygame.Rect(x - CANDLE_WIDTH // 2, body_top, CANDLE_WIDTH, max(1, body_height))
    pygame.draw.rect(screen, color, body_rect)
    pygame.draw.rect(screen, border_color, body_rect, 1)


def draw_stock_chart(screen, font, stock, chart_x, chart_y, visible_candles=50):
    """Draw candlestick chart for a stock."""
    # Get price range for scaling
    candles = stock.candles
    if not candles:
        return

    # Use recent candles
    visible_candles_list = candles[-visible_candles:]

    if not visible_candles_list:
        return

    min_price = min(c.low for c in visible_candles_list)
    max_price = max(c.high for c in visible_candles_list)
    price_range = max_price - min_price
    if price_range == 0:
        price_range = 1

    # Calculate scale: map price range to chart height
    chart_available_height = CHART_HEIGHT - 2 * CHART_PADDING
    height_scale = chart_available_height / price_range

    # Draw chart background
    chart_rect = pygame.Rect(chart_x, chart_y, CHART_WIDTH, CHART_HEIGHT)
    pygame.draw.rect(screen, light_gray, chart_rect)
    pygame.draw.rect(screen, black, chart_rect, 1)

    # Draw grid lines
    grid_y = chart_y + CHART_PADDING
    grid_height = CHART_HEIGHT - 2 * CHART_PADDING
    num_grid_lines = 5
    for i in range(num_grid_lines + 1):
        y_pos = grid_y + (grid_height * i // num_grid_lines)
        pygame.draw.line(screen, gray, (chart_x, y_pos), (chart_x + CHART_WIDTH, y_pos), 1)

    # Calculate candle positions
    total_candle_width = CANDLE_WIDTH + CANDLE_SPACING
    max_candles_fit = CHART_WIDTH // total_candle_width

    # Render candles
    candle_x = chart_x + CHART_PADDING
    for candle in visible_candles_list:
        if candle_x + CANDLE_WIDTH > chart_x + CHART_WIDTH - CHART_PADDING:
            break

        draw_candle(
            screen,
            candle_x,
            chart_y,
            (candle.open, candle.high, candle.low, candle.close),
            height_scale,
            min_price,
            max_price
        )
        candle_x += total_candle_width

    # Draw price axis on left
    price_y = chart_y + CHART_PADDING
    for i in range(num_grid_lines + 1):
        price_pos = max_price - (price_range * i // num_grid_lines)
        price_text = f"${price_pos:.1f}"
        text_surface = font.render(price_text, True, black)
        screen.blit(text_surface, (chart_x - 50, price_y - 5 + (grid_height * i // num_grid_lines)))


def draw_pattern_info(screen, font, stock, x, y):
    """Draw pattern information above the chart.

    Shows pattern name, category, and progress bars when a pattern is active.
    """
    if stock.current_pattern_name is None:
        return

    pattern_name = stock.current_pattern_name
    pattern_info = pattern_assets.get_pattern_info(pattern_name)

    if pattern_info is None:
        return

    # Extract pattern info
    display_name, category, color_category = pattern_info
    color = pattern_assets.get_pattern_color(pattern_name)

    # Draw pattern name
    title_text = f"PATTERN: {display_name}"
    title_surface = font.render(title_text, True, color)
    screen.blit(title_surface, (x, y))

    # Draw category
    category_text = f"CATEGORY: {category}"
    category_surface = font.render(category_text, True, (100, 100, 100))
    screen.blit(category_surface, (x, y + 20))

    # Draw pattern progress bar
    if stock._active_segment:
        remaining_ticks, _ = stock._active_segment
        total_ticks, _ = stock._active_segment

        # Calculate progress
        if hasattr(stock, '_pattern_total_ticks'):
            total_pattern_ticks = stock._pattern_total_ticks
        else:
            total_pattern_ticks = 20  # Default

        # Get current progress from queue + active
        queue_ticks = sum(q[0] for q in stock._pattern_queue)
        active_ticks = remaining_ticks

        total_to_complete = total_pattern_ticks
        completed = total_to_complete - (queue_ticks + active_ticks)
        if completed < 0:
            completed = 0

        progress_pct = completed / total_to_complete if total_to_complete > 0 else 0

        # Draw progress bar background
        bar_width = 200
        bar_height = 12
        bar_x = x
        bar_y = y + 45

        # Bar background
        pygame.draw.rect(screen, PATTERN_PROGRESS_BG,
                        (bar_x, bar_y, bar_width, bar_height))
        # Border
        pygame.draw.rect(screen, black,
                        (bar_x, bar_y, bar_width, bar_height), 1)

        # Progress fill
        fill_width = int(bar_width * progress_pct)
        pygame.draw.rect(screen, color,
                        (bar_x, bar_y, fill_width, bar_height))

        # Draw individual tick indicators
        num_indicators = min(10, total_pattern_ticks)
        indicator_spacing = bar_width // num_indicators

        for i in range(num_indicators):
            indicator_x = bar_x + (i * indicator_spacing) + indicator_spacing // 2
            # Draw tick line
            pygame.draw.line(screen, gray, (indicator_x, bar_y - 3),
                           (indicator_x, bar_y + bar_height + 3), 1)

        # Draw percentage text
        pct_text = f"{int(progress_pct * 100)}%"
        pct_surface = font.render(pct_text, True, black)
        screen.blit(pct_surface, (bar_x + bar_width + 10, bar_y))


def draw_candle_progress(screen, stock, x, y, candle_width=8, spacing=3):
    """Draw a summary of the current candle formation progress."""
    if not stock.candles and stock._current_candle is None:
        return

    current = stock._current_candle
    if current is None:
        return

    # Draw current candle progress indicator
    candle_base_y = y + 10
    candle_base_x = x

    # Draw candle outline
    body_height = 20
    body_width = candle_width

    # Current candle progress (based on ticks vs expected ticks per candle)
    ticks_per_candle = 5  # Default
    progress = min(current.tick / ticks_per_candle, 1.0) if ticks_per_candle > 0 else 1.0

    # Draw body with progress opacity
    alpha = int(255 * progress)

    if current.is_bullish():
        body_color = (0, min(255, 150 + 100 * progress), 0, alpha)
    elif current.is_bearish():
        body_color = (min(255, 200 + 55 * progress), 0, 0, alpha)
    else:
        body_color = (128, 128, 128, alpha)

    # Draw the candle body
    body_rect = pygame.Rect(candle_base_x, candle_base_y - body_height,
                           body_width, body_height)
    pygame.draw.rect(screen, body_color[:3], body_rect)
    pygame.draw.rect(screen, black, body_rect, 1)

    # Draw progress indicator
    if progress < 1.0:
        progress_bar_x = candle_base_x + body_width + 5
        progress_bar_y = candle_base_y - body_height // 2
        bar_width = 30
        bar_height = 4

        # Background
        pygame.draw.rect(screen, PATTERN_PROGRESS_BG,
                        (progress_bar_x, progress_bar_y, bar_width, bar_height))
        # Fill
        fill_width = int(bar_width * progress)
        pygame.draw.rect(screen, (0, 128, 255),
                        (progress_bar_x, progress_bar_y, fill_width, bar_height))


def inject_pattern_for_stock(stock, pattern_key):
    """Inject a pattern into a stock and return the pattern name."""
    try:
        stock.inject_named_pattern(pattern_key)
        return pattern_key
    except KeyError:
        return None


def draw_stock_summary(screen, font, stock, x, y):
    """Draw stock summary info below the chart."""
    # Current price - color based on recent trend
    price_text = f"Price: ${stock.price:.2f}"
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

    # Pattern status
    if stock.current_pattern_name:
        pattern_text = f"Pattern: {stock.current_pattern_name.replace('_', ' ').title()}"
        pattern_surface = font.render(pattern_text, True, (0, 100, 200))
        screen.blit(pattern_surface, (x, y + 40))


def run(game):
    pygame.init()
    display_info = pygame.display.Info()
    screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
    SCREEN_W, SCREEN_H = display_info.current_w, display_info.current_h
    game_surface = pygame.Surface((GAME_W, GAME_H))

    assets = load_all_assets()
    clock = pygame.time.Clock()
    player = game.players[0]
    
    game_clock = GameClock()
    dt = 16 

    state = "menu"
    running = True

    selected_char = 0
    anim_frame = 0
    ticker_offset = 0
    
    market_open = False
    shop_open = False
    buy_buttons = []
    
    owned_desks = ["desk1"]
    confirm_open = False
    pending_item = None
    
    last_update = pygame.time.get_ticks()
    stock_prev_prices = {stock.name: stock.price for stock in game.stocks}
    
    s_btn = c_btn = q_btn = pygame.Rect(0,0,0,0)
    cards, b_btn, ok_btn = [], pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0)
    menu_btn_rect = pygame.Rect(GAME_W - 150, 15, 130, 45)
    yes_btn = no_btn = pygame.Rect(0,0,0,0)

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
                    if event.key == pygame.K_ESCAPE: 
                        if confirm_open: confirm_open = False 
                        else:
                            state = "menu"
                            market_open = False
                            shop_open = False
                    elif event.key == pygame.K_q and market_open: 
                        market_open = False
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
                                owned_desks.append(pending_item["id"])
                                assets["current_desk_id"] = pending_item["id"]
                            confirm_open = False
                        elif no_btn.collidepoint(gpt):
                            confirm_open = False
                            
                    
                    else:
                        if menu_btn_rect.collidepoint(gpt):
                            state = "menu"
                            market_open = False
                            shop_open = False
                            
                        if shop_open:
                            for btn_rect, item, btn_text in buy_buttons:
                                if btn_rect.collidepoint(gpt):
                                    if btn_text == "Buy" and player.cash >= item["price"]:
                                        
                                        confirm_open = True
                                        pending_item = item
                                    elif btn_text == "Equip":
                                        
                                        assets["current_desk_id"] = item["id"]

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

            game_surface.blit(assets["bg"], (0, 0))
            current_desk = assets["desks"].get(assets["current_desk_id"])
            if current_desk:
                game_surface.blit(current_desk, assets["desk_rect"])

            for prop in MAP_PROPS:
                prop_img = assets["props"].get(prop["type"])
                if prop_img:
                    game_surface.blit(prop_img, (prop["x"], prop["y"]))

            menu_btn_rect = draw_top_bar(
                game_surface, assets["hud_font"], assets["small_font"], assets["hud_bold_font"],player, 
                assets["icon_coin"], ticker_offset, game.stocks, stock_prev_prices
            )
            ticker_offset -= 1.5
            if ticker_offset < -(len(game.stocks) * 180): ticker_offset = 0
            
            if not market_open and not shop_open and not confirm_open:
                anim_frame = handle_player_movement(player, 3.5, anim_frame)
                game_clock.update(dt) 

            draw_clock_overlay(game_surface, assets["small_font"], assets["hud_font"], game_clock)

            p_rect = draw_player(
                game_surface, player, anim_frame, 
                assets["all_char_anims"][selected_char], assets["char_images"][selected_char]
            )

            if p_rect.colliderect(assets["computer_rect"].inflate(100, 100)) and not market_open and not shop_open:
                game_surface.blit(assets["hud_font"].render("Press E to interact", True, GREEN), (assets["computer_rect"].x - 20, assets["computer_rect"].y - 60))

            if market_open:
                draw_market_overlay(game_surface, assets["body_font"], assets["hud_font"], assets["small_font"], game.stocks)
                
            if shop_open:
                buy_buttons = draw_shop_overlay(
                    game_surface, assets["body_font"], assets["small_font"], player, 
                    assets["icon_coin"], assets["desks"], owned_desks, assets["current_desk_id"]
                )
                
            if confirm_open and pending_item:
                yes_btn, no_btn = draw_confirmation_screen(
                    game_surface, assets["body_font"], assets["small_font"], 
                    f"Buy {pending_item['name']}?"
                )

        scaled = pygame.transform.scale(game_surface, (SCREEN_W, SCREEN_H))
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        
        # Capture delta time 
        dt = clock.tick(60)

    pygame.quit()
    sys.exit()