import pygame

def move_with_collision(entity, dx, dy, wall_mask, feet_mask, props_collision=None, char_width=64, char_height=64, custom_offset_x=None, custom_offset_y=None, placed_props=None, placed_masks=None):
    if props_collision is None: 
        props_collision = []
    if placed_props is None:
        placed_props = []
    if placed_masks is None:
        placed_masks = {}
        
    feet_w, feet_h = feet_mask.get_size()
    offset_x = custom_offset_x if custom_offset_x is not None else (char_width / 2) - (feet_w / 2)
    offset_y = custom_offset_y if custom_offset_y is not None else char_height - feet_h
    
    def is_collision(test_x, test_y):
        # 1. Wall Collision
        if wall_mask.overlap(feet_mask, (test_x, test_y)):
            return True
            
        # 2. Base Map Props (Tables, Lockers)
        for p in props_collision:
            rel_x = test_x - int(p["x"])
            rel_y = test_y - int(p["y"])
            if p["mask"].overlap(feet_mask, (rel_x, rel_y)):
                return True
                
        # 3. Newly Placed Props (USING FULL MASK!)
        for p in placed_props:
            full_mask = placed_masks.get(p["id"])
            if full_mask:
                rel_x = test_x - int(p["x"])
                rel_y = test_y - int(p["y"])
                if full_mask.overlap(feet_mask, (rel_x, rel_y)):
                    return True
                    
        return False

    # Test X Axis
    if dx != 0:
        entity.x += dx
        test_x = int(entity.x + offset_x)
        test_y = int(entity.y + offset_y)
        
        if is_collision(test_x, test_y):
            entity.x -= dx

    # Test Y Axis
    if dy != 0:
        entity.y += dy
        test_x = int(entity.x + offset_x)
        test_y = int(entity.y + offset_y)
        
        if is_collision(test_x, test_y):
            entity.y -= dy
            
    # Save for debugging
    entity.hitbox = pygame.Rect(int(entity.x + offset_x), int(entity.y + offset_y), feet_w, feet_h)