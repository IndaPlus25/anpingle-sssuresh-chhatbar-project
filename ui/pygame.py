import pygame
import sys

GAME_W, GAME_H = 600, 400

####################
# colors

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

####################

def run(game):
    pygame.init()

    # Get real display resolution for fullscreen
    display_info = pygame.display.Info()
    SCREEN_W, SCREEN_H = display_info.current_w, display_info.current_h

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN)
    pygame.display.set_caption("Hedge Fund Game")

    # All drawing happens on this fixed 600x400 surface, then scaled up
    game_surface = pygame.Surface((GAME_W, GAME_H))

    background = pygame.image.load("office_bg.png").convert()
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

        game_surface.blit(background, (0, 0))

        font = pygame.font.SysFont(None, 30)
        cash_text = font.render(f"Cash: {player.cash}", True, blue)
        game_surface.blit(cash_text, (20, 20))

        player_rect = pygame.Rect(player.x, player.y, 40, 40)
        pygame.draw.rect(game_surface, red, player_rect)

        #pygame.draw.rect(game_surface, black, computer_rect)
        #computer_label = font.render("COMPUTER", True, white)
        #game_surface.blit(computer_label, (computer_rect.x - 5, computer_rect.y - 25))

        distance_x = abs(player_rect.centerx - computer_rect.centerx)
        distance_y = abs(player_rect.centery - computer_rect.centery)
        near_computer = distance_x < interaction_distance and distance_y < interaction_distance

        if near_computer and not market_open:
            prompt = font.render("Press E to interact", True, green)
            game_surface.blit(prompt, (computer_rect.x - 10, computer_rect.y - 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_e and near_computer and not market_open:
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
            market_box = pygame.Rect(80, 100, 440, 220)
            pygame.draw.rect(game_surface, black, market_box)
            pygame.draw.rect(game_surface, blue, market_box, 3)

            header = font.render("Stock Market", True, green)
            game_surface.blit(header, (market_box.x + 15, market_box.y + 12))

            close_text = font.render("Press Q to close", True, white)
            game_surface.blit(close_text, (market_box.x + 15, market_box.y + 180))

            row_y = market_box.y + 50
            for stock in game.stocks:
                stock_line = font.render(f"{stock.name}: ${stock.price:.2f}", True, white)
                game_surface.blit(stock_line, (market_box.x + 15, row_y))
                row_y += 35

        # Scale the 600x400 game surface up to fill the screen
        scaled = pygame.transform.scale(game_surface, (SCREEN_W, SCREEN_H))
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()