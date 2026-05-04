import pygame
import sys

w, h = 600, 400

####################
# colors

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_green = (144, 238, 144)  # light green for bullish candles
light_red = (255, 182, 193)    # light red for bearish candles
dark_green = (0, 100, 0)       # dark green border for bullish
dark_red = (139, 0, 0)         # dark red border for bearish
gray = (128, 128, 128)
light_gray = (220, 220, 220)

####################

# Chart settings
CHART_WIDTH = 400
CHART_HEIGHT = 150
CHART_PADDING = 10
CANDLE_WIDTH = 8
CANDLE_SPACING = 3


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
    close_y = price_to_y(close_p)
    high_y = price_to_y(high)
    low_y = price_to_y(low)

    # Determine color
    if close >= open:
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


def run(game):
    pygame.init()
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Hedge Fund Game")
    clock = pygame.time.Clock()
    move_speed = 5

    running = True
    player = game.players[0]
    computer_rect = pygame.Rect(100, 250, 60, 20)
    interaction_distance = 80
    market_open = False
    last_update_time = pygame.time.get_ticks()


    while running:
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > 1000:
            game.update_stocks()
            last_update_time = current_time

        screen.fill(white)

        font = pygame.font.SysFont(None, 30)
        cash_text = font.render(f"Cash: {player.cash}", True, blue)
        screen.blit(cash_text, (20, 20))

        player_rect = pygame.Rect(player.x, player.y, 40, 40)
        pygame.draw.rect(screen, red, player_rect)

        pygame.draw.rect(screen, black, computer_rect)
        computer_label = font.render("COMPUTER", True, white)
        screen.blit(computer_label, (computer_rect.x - 5, computer_rect.y - 25))

        distance_x = abs(player_rect.centerx - computer_rect.centerx)
        distance_y = abs(player_rect.centery - computer_rect.centery)
        near_computer = distance_x < interaction_distance and distance_y < interaction_distance

        if near_computer and not market_open:
            prompt = font.render("Press E to interact", True, green)
            screen.blit(prompt, (computer_rect.x - 10, computer_rect.y - 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and near_computer and not market_open:
                    market_open = True
                elif event.key == pygame.K_q and market_open:
                    market_open = False



        if not market_open:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player.move(-move_speed)
            elif keys[pygame.K_d]:
                player.move(move_speed)
        else:
            market_box = pygame.Rect(80, 100, 440, 380)
            pygame.draw.rect(screen, black, market_box)
            pygame.draw.rect(screen, blue, market_box, 3)

            header = font.render("Stock Market", True, green)
            screen.blit(header, (market_box.x + 15, market_box.y + 12))

            close_text = font.render("Press q to close", True, white)
            screen.blit(close_text, (market_box.x + 15, market_box.y + 340))

            # Draw candlestick charts for each stock
            stock_x = market_box.x + 15
            stock_y = market_box.y + 40

            for stock in game.stocks:
                # Draw stock name
                stock_name_text = font.render(stock.name, True, white)
                screen.blit(stock_name_text, (stock_x, stock_y))

                # Draw current price
                price_text = font.render(f"${stock.price:.2f}", True, blue)
                screen.blit(price_text, (stock_x + 60, stock_y))

                # Draw candlestick chart (smaller for multiple stocks)
                draw_stock_chart(screen, font, stock, stock_x, stock_y + 20, visible_candles=30)

                # Move to next stock (add spacing)
                stock_y += CHART_HEIGHT - 20


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()