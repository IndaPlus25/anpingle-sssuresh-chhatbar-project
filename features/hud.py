import pygame
from ui.constants import GAME_W, GOLD, WHITE, GREEN, RED, LGRAY

def draw_stock_ticker(game_surface, small_font, bold_font, ticker_offset, stocks, stock_prev_prices):
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
            
            name_surf = bold_font.render(stock.name.upper(), True, WHITE)
            game_surface.blit(name_surf, (tx, 12)) 
            
            color = GREEN if is_up else RED
            arrow_x = tx + name_surf.get_width() + 10
            
            pts = [(arrow_x, 27), (arrow_x+8, 17), (arrow_x+16, 27)] if is_up else [(arrow_x, 17), (arrow_x+8, 27), (arrow_x+16, 17)]
            pygame.draw.polygon(game_surface, color, pts)
            
            change_surf = small_font.render(f"{'+' if is_up else ''}{change_pct:.1f}%", True, color)
            game_surface.blit(change_surf, (arrow_x + 22, 10))
            
            tx += ticker_spacing
            
    game_surface.set_clip(None)

def draw_top_bar(game_surface, hud_font, small_font, bold_font, player, icon_coin, ticker_offset, stocks, stock_prev_prices):
    pygame.draw.rect(game_surface, (20, 20, 35), (0, 0, GAME_W, 50))
    pygame.draw.rect(game_surface, (40, 40, 60), (0, 48, GAME_W, 2))
    
    if icon_coin: game_surface.blit(icon_coin, (12, 7))
    
    cash_val = player.cash
    
    if cash_val >= 1000000:
        rounded_m = (cash_val // 100000) / 10.0
        cash_text_str = f"${rounded_m:.1f}M"
    else:

        rounded_k = cash_val // 1000
        cash_text_str = f"${rounded_k}K"
        
    game_surface.blit(hud_font.render(cash_text_str, True, GOLD), (70, 5))
    
    draw_stock_ticker(game_surface, small_font, bold_font, ticker_offset, stocks, stock_prev_prices)
    
    menu_btn = pygame.Rect(GAME_W - 55, 8, 45, 34)
    pygame.draw.rect(game_surface, (40, 40, 60), menu_btn, border_radius=4)
    menu_lines = small_font.render("≡", True, LGRAY)
    game_surface.blit(menu_lines, menu_lines.get_rect(center=menu_btn.center))
    return menu_btn
def draw_clock_overlay(game_surface, small_font, hud_font, game_clock):
    #Draws clock
    date_str = game_clock.get_date_string()
    time_str = game_clock.get_time_string()

    # Render Text
    date_surf = small_font.render(date_str, True, (200, 200, 220)) # LGRAY
    time_surf = hud_font.render(time_str, True, (255, 255, 255))   # WHITE

    # Box Dimensions 
    box_w = max(date_surf.get_width(), time_surf.get_width()) + 30
    box_h = 70
    box_x = 20
    box_y = 60 

    box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

    # Draw Background
    pygame.draw.rect(game_surface, (50, 55, 75), box_rect, border_radius=6)
    pygame.draw.rect(game_surface, (30, 30, 45), box_rect, 4, border_radius=6)
    pygame.draw.rect(game_surface, (100, 105, 130), box_rect.inflate(-4, -4), 2, border_radius=6)

    # Draw the Text centered inside the box
    game_surface.blit(date_surf, (box_rect.centerx - date_surf.get_width() // 2, box_y + 8))
    game_surface.blit(time_surf, (box_rect.centerx - time_surf.get_width() // 2, box_y + 32))