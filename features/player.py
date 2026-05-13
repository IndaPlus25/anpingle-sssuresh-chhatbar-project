import pygame
from ui.constants import GAME_W, GAME_H
from features.collision import move_with_collision

def handle_player_movement(player, speed, anim_frame, assets):
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    is_moving = False

    if keys[pygame.K_w] or keys[pygame.K_UP]: 
        dy -= speed
        player.direction = "north"
        is_moving = True
    if keys[pygame.K_s] or keys[pygame.K_DOWN]: 
        dy += speed
        player.direction = "south"
        is_moving = True
    if keys[pygame.K_a] or keys[pygame.K_LEFT]: 
        dx -= speed
        player.direction = "west"
        is_moving = True
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
        dx += speed
        player.direction = "east"
        is_moving = True

    if dx < 0 and dy < 0: player.direction = "northwest"
    elif dx > 0 and dy < 0: player.direction = "northeast"
    elif dx < 0 and dy > 0: player.direction = "southwest"
    elif dx > 0 and dy > 0: player.direction = "southeast"


    if dx != 0 and dy != 0:
        dx *= 0.7071
        dy *= 0.7071
    player.is_moving = is_moving
    if is_moving:
        move_with_collision(player, dx, dy, assets["walls_mask"], assets["feet_mask"], props_collision=assets["props_collision"],char_width=64, char_height=64, custom_offset_x=30, custom_offset_y=65)
        anim_frame = (anim_frame + 0.15) % 6
    else:
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