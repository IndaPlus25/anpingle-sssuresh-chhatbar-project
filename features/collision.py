import pygame

def move_with_collision(entity, dx, dy, wall_mask, feet_mask, props_collision=None, char_width=64, char_height=64, custom_offset_x=None, custom_offset_y=None):
    if props_collision is None: 
        props_collision = []
        
    feet_w, feet_h = feet_mask.get_size()
    offset_x = custom_offset_x if custom_offset_x is not None else (char_width / 2) - (feet_w / 2)
    offset_y = custom_offset_y if custom_offset_y is not None else char_height - feet_h
    
    # Test X Axis
    if dx != 0:
        entity.x += dx
        test_x = int(entity.x + offset_x)
        test_y = int(entity.y + offset_y)
        
        hit_wall = wall_mask.overlap(feet_mask, (test_x, test_y))
        
        hit_prop = False
        for p in props_collision:
            rel_x = test_x - int(p["x"])
            rel_y = test_y - int(p["y"])
            
            if p["mask"].overlap(feet_mask, (rel_x, rel_y)):
                hit_prop = True
                break
                
        if hit_wall or hit_prop:
            entity.x -= dx # 

    #Y Axis
    if dy != 0:
        entity.y += dy
        test_x = int(entity.x + offset_x)
        test_y = int(entity.y + offset_y)
        
        hit_wall = wall_mask.overlap(feet_mask, (test_x, test_y))
        
        hit_prop = False
        for p in props_collision:
            rel_x = test_x - int(p["x"])
            rel_y = test_y - int(p["y"])
            
            if p["mask"].overlap(feet_mask, (rel_x, rel_y)):
                hit_prop = True
                break
                
        if hit_wall or hit_prop:
            entity.y -= dy # Undo Y
            
    # Save for debugging
    entity.hitbox = pygame.Rect(int(entity.x + offset_x), int(entity.y + offset_y), feet_w, feet_h)