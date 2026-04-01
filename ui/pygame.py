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

    running = True
    while running:
        screen.fill(white)
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Cash: {game.players[0].cash}", True, blue)
        screen.blit(text,(20,20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()