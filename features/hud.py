import pygame
from ui.constants import GAME_W, GOLD, WHITE, GREEN, RED, LGRAY

def draw_stock_ticker(game_surface, small_font, ticker_offset, stocks, stock_prev_prices):
    bar_height = 50
    ticker_start_x, ticker_end_x = 240, GAME_W - 65
    
    clip_rect = pygame.Rect(ticker_start_x, 0, ticker_end_x - ticker_start_x, bar_height)
    game_surface.set_clip(clip_rect)
    
    ticker_spacing = 180
    total_ticker_width = len(stocks) * ticker_spacing
    
    for loop in range(2):
        tx = ticker_start_x + ticker_offset + (loop * total_ticker_width)
        for stock in stocks:
            prev = stock_prev_prices.get(stock.name, stock.price)
            change_pct = ((stock.price - prev) / prev * 100) if prev > 0 else 0
            is_up = change_pct >= 0
            
            name_surf = small_font.render(stock.name.upper(), True, WHITE)
            game_surface.blit(name_surf, (tx, 8))
            
            color = GREEN if is_up else RED
            arrow_x = tx + name_surf.get_width() + 8
            pts = [(arrow_x, 29), (arrow_x+8, 19), (arrow_x+16, 29)] if is_up else [(arrow_x, 19), (arrow_x+8, 29), (arrow_x+16, 19)]
            pygame.draw.polygon(game_surface, color, pts)
            
            change_surf = small_font.render(f"{'+' if is_up else ''}{change_pct:.1f}%", True, color)
            game_surface.blit(change_surf, (arrow_x + 20, 8))
            tx += ticker_spacing
            
    game_surface.set_clip(None)

def draw_top_bar(game_surface, hud_font, small_font, player, icon_coin, ticker_offset, stocks, stock_prev_prices):
    pygame.draw.rect(game_surface, (20, 20, 35), (0, 0, GAME_W, 50))
    pygame.draw.rect(game_surface, (40, 40, 60), (0, 48, GAME_W, 2))
    
    if icon_coin: game_surface.blit(icon_coin, (12, 7))
    
    cash_val = player.cash
    cash_text_str = f"${cash_val/1000000:.1f}M" if cash_val >= 1000000 else f"${cash_val/1000:.0f}K"
    game_surface.blit(hud_font.render(cash_text_str, True, GOLD), (70, 5))
    
    draw_stock_ticker(game_surface, small_font, ticker_offset, stocks, stock_prev_prices)
    
    menu_btn = pygame.Rect(GAME_W - 55, 8, 45, 34)
    pygame.draw.rect(game_surface, (40, 40, 60), menu_btn, border_radius=4)
    menu_lines = small_font.render("≡", True, LGRAY)
    game_surface.blit(menu_lines, menu_lines.get_rect(center=menu_btn.center))
    return menu_btn