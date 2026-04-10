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

    pygame.init()
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Hedge Fund Game")
    clock = pygame.time.Clock()
    move_speed = 5

    running = True
    player = game.players[0]
    while running:
        screen.fill(white)
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Cash: {player.cash}", True, blue)
        screen.blit(text, (20, 20))

        player_rect = pygame.Rect(player.x, player.y, 40, 40)
        pygame.draw.rect(screen, red, player_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.move(-move_speed)
        elif keys[pygame.K_d]:
            player.move(move_speed)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()