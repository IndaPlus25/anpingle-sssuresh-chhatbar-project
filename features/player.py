import pygame
from ui.constants import GAME_W, GAME_H

def handle_player_movement(player, move_speed, anim_frame):
    """player movement"""
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    
    if keys[pygame.K_a]: dx = -move_speed
    if keys[pygame.K_d]: dx = move_speed
    if keys[pygame.K_w]: dy = -move_speed
    if keys[pygame.K_s]: dy = move_speed
    
    player.x = max(0, min(player.x + dx, GAME_W - 64))
    player.y = max(0, min(player.y + dy, GAME_H - 64))

    if dx != 0 or dy != 0:
        player.is_moving = True
        dir_str = ""
        if dy < 0: dir_str += "north"
        elif dy > 0: dir_str += "south"
        if dx < 0: dir_str += "west"
        elif dx > 0: dir_str += "east"
        player.direction = dir_str
        anim_frame = (anim_frame + 0.12) % 6
    else:
        player.is_moving = False
        anim_frame = 0
        
    return anim_frame

def draw_player(game_surface, player, anim_frame, current_anims, fallback_image):
    """Draws the player"""
    p_rect = pygame.Rect(player.x, player.y, 64, 64)
    
    if current_anims:
        d = getattr(player, 'direction', 'south')
        if player.is_moving and current_anims["walk"].get(d):
            img = current_anims["walk"][d][int(anim_frame)]
        else:
            img = current_anims["idle"].get(d) or fallback_image
        game_surface.blit(img, p_rect)
    else:
        if fallback_image: game_surface.blit(fallback_image, p_rect)
        
    return p_rect