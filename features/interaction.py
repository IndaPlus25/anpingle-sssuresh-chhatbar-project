import pygame
from ui.constants import GAME_W, GAME_H, BLUE, WHITE

def draw_button(surf, rect, text, font, color=BLUE, text_color=WHITE, radius=8, icon=None):
    mx, my = pygame.mouse.get_pos()
    screen = pygame.display.get_surface()
    scale_x = GAME_W / screen.get_width()
    scale_y = GAME_H / screen.get_height()
    gx, gy = int(mx * scale_x), int(my * scale_y)

    hovered = rect.collidepoint(gx, gy)
    col = tuple(min(255, c + 40) for c in color) if hovered else color

    pygame.draw.rect(surf, col, rect, border_radius=radius)
    pygame.draw.rect(surf, WHITE, rect, 2, border_radius=radius)

    if icon:
        text_surf = font.render(text, True, text_color)
        total_w = icon.get_width() + 10 + text_surf.get_width()
        start_x = rect.centerx - total_w // 2
        surf.blit(icon, (start_x, rect.centery - icon.get_height() // 2))
        surf.blit(text_surf, (start_x + icon.get_width() + 10, rect.centery - text_surf.get_height() // 2))
    else:
        label = font.render(text, True, text_color)
        surf.blit(label, label.get_rect(center=rect.center))
    return hovered

def mouse_clicked_in_game(event):
    screen = pygame.display.get_surface()
    scale_x = GAME_W / screen.get_width()
    scale_y = GAME_H / screen.get_height()
    return int(event.pos[0] * scale_x), int(event.pos[1] * scale_y)