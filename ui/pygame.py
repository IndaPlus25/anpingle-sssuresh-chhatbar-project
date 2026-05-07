import pygame
import sys

from .constants import *
from .screens import draw_menu, draw_char_select, draw_market_overlay, draw_shop_overlay, draw_confirmation_screen
from features.interaction import mouse_clicked_in_game
from features.hud import draw_top_bar
from features.assets import load_all_assets
from features.player import handle_player_movement, draw_player

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
                game_surface, assets["hud_font"], assets["small_font"], player, 
                assets["icon_coin"], ticker_offset, game.stocks, stock_prev_prices
            )
            ticker_offset -= 1.5
            if ticker_offset < -(len(game.stocks) * 180): ticker_offset = 0
            
            if not market_open and not shop_open and not confirm_open:
                anim_frame = handle_player_movement(player, 3.5, anim_frame)
                
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
        clock.tick(60)

    pygame.quit()
    sys.exit()