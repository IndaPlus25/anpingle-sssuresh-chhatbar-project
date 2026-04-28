import pygame
import sys

w,h = 600,400

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
            market_box = pygame.Rect(80, 100, 440, 220)
            pygame.draw.rect(screen, black, market_box)
            pygame.draw.rect(screen, blue, market_box, 3)

            header = font.render("Stock Market", True, green)
            screen.blit(header, (market_box.x + 15, market_box.y + 12))

            close_text = font.render("Press q to close", True, white)
            screen.blit(close_text, (market_box.x + 15, market_box.y + 180))

            row_y = market_box.y + 50
            for stock in game.stocks:
                stock_line = font.render(f"{stock.name}: ${stock.price:.2f}", True, white)
                screen.blit(stock_line, (market_box.x + 15, row_y))
                row_y += 35


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()