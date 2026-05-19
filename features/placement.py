import pygame

def check_placement_valid(x, y, item_id, assets, placed_props):
    """Checks if the item's feet mask collides with walls or other props."""
    item_mask = assets.get("placeable_masks", {}).get(item_id)
    if not item_mask: 
        return True # Fallback if mask fails
        
    # 1. Check Wall Collision
    walls_mask = assets.get("walls_mask")
    if walls_mask:
        offset = (int(x), int(y))
        if walls_mask.overlap(item_mask, offset):
            return False
            
    # 2. Check Existing Map Props (Lockers, tables, etc.)
    for prop in assets.get("props_collision", []):
        prop_mask = prop["mask"]
        offset = (int(prop["x"] - x), int(prop["y"] - y))
        if item_mask.overlap(prop_mask, offset):
            return False

    # 3. Check Other Player-Placed Props
    for prop in placed_props:
        prop_mask = assets["placeable_masks"].get(prop["id"])
        if prop_mask:
            offset = (int(prop["x"] - x), int(prop["y"] - y))
            if item_mask.overlap(prop_mask, offset):
                return False
                
    return True

def draw_placement_preview(surface, item_id, x, y, is_valid, assets):
    """Draws a tinted preview of the item with professional alignment arrows."""
    img = assets.get("placeables", {}).get(item_id)
    if not img: return
    
    # Create a tinted copy of the image
    preview = img.copy()
    tint = (0, 255, 50, 120) if is_valid else (255, 0, 50, 150)
    preview.fill(tint, special_flags=pygame.BLEND_RGBA_MULT)
    
    # Draw the item
    surface.blit(preview, (x, y))
    
    # Draw UX movement arrows around it
    w, h = img.get_size()
    cx, cy = x + w // 2, y + h // 2
    offset = max(w, h) // 2 + 10
    
    arrow_color = (255, 255, 255)
    # Up, Down, Left, Right arrows
    pygame.draw.polygon(surface, arrow_color, [(cx, cy - offset), (cx - 5, cy - offset + 5), (cx + 5, cy - offset + 5)])
    pygame.draw.polygon(surface, arrow_color, [(cx, cy + offset), (cx - 5, cy + offset - 5), (cx + 5, cy + offset - 5)])
    pygame.draw.polygon(surface, arrow_color, [(cx - offset, cy), (cx - offset + 5, cy - 5), (cx - offset + 5, cy + 5)])
    pygame.draw.polygon(surface, arrow_color, [(cx + offset, cy), (cx + offset - 5, cy - 5), (cx + offset - 5, cy + 5)])