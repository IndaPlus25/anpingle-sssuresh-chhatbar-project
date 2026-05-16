import pygame

class IRSAgent:
    def __init__(self, start_x, start_y, desk_x, desk_y):
        self.x = start_x
        self.y = start_y
        
        self.target_x = desk_x
        self.target_y = desk_y
        
        self.speed = 0.8 
        self.state = "approaching" 
        self.speech_text = "I'm here for the books."
        
        # Animation Variables
        self.direction = "north"
        self.anim_frame = 0

    def update(self, dt, assets):
        """Moves the agent and returns True if they reached the desk via MASK collision."""
        feet_y = self.y + 32 
        
        if self.state == "approaching":
            dx = self.target_x - self.x
            dy = self.target_y - feet_y
            dist = (dx**2 + dy**2)**0.5
            
            # --- MASK COLLISION CHECK ---
            reached = False
            desk_rect = assets.get("desk_rect")
            desk_id = assets.get("current_desk_id")
            desk_img = assets["desks"].get(desk_id)
            
            if desk_rect and desk_img and "feet_mask" in assets:
                desk_mask = pygame.mask.from_surface(desk_img)
                feet_mask = assets["feet_mask"]
                
                # Agent feet top-left coordinate (assuming 32x16 mask centered at bottom of 64x64 sprite)
                feet_x_topleft = self.x - 16
                feet_y_topleft = self.y + 16
                
                offset_x = feet_x_topleft - desk_rect.x
                offset_y = feet_y_topleft - desk_rect.y
                
                # If the agent's feet mask overlaps the desk mask, stop moving!
                if desk_mask.overlap(feet_mask, (int(offset_x), int(offset_y))):
                    reached = True
                    
            # Fallback to distance check just in case the mask misses
            if reached or dist < 5: 
                self.anim_frame = 0 # Stand still
                return True 
            else:
                move_x = (dx / dist) * self.speed
                move_y = (dy / dist) * self.speed
                self.x += move_x
                self.y += move_y
                
                # Determine Animation Direction
                if abs(move_x) > abs(move_y):
                    self.direction = "east" if move_x > 0 else "west"
                else:
                    self.direction = "south" if move_y > 0 else "north"
                    
                self.anim_frame = (self.anim_frame + 0.1) % 6
                
        elif self.state == "leaving":
            self.y += self.speed * 3 
            self.direction = "south"
            self.anim_frame = (self.anim_frame + 0.2) % 6
            
        return False

    def draw(self, surface, font, anims):
        """Draws the Agent using your custom load_json_animations structure."""
        rect = pygame.Rect(self.x - 32, self.y - 32, 64, 64)
        drawn = False
        
        if anims:
            # Your loader perfectly mapped these to "idle" and "walk", so we just use them!
            if self.state == "approaching" and self.anim_frame == 0:
                anim_dict = anims.get("idle", {})
            else:
                anim_dict = anims.get("walk", {})
            
            # Grab the frames for the current direction (e.g., "east")
            img = anim_dict.get(self.direction)
            
            if type(img) == list and len(img) > 0: 
                # Safely loop using the actual number of frames so it never crashes!
                safe_index = int(self.anim_frame) % len(img)
                img = img[safe_index]
                
            if img:
                img = pygame.transform.scale(img, (64, 64))
                surface.blit(img, rect)
                drawn = True
                
        if not drawn:
            # FALLBACK: If direction is missing, draw a MAGENTA box to debug
            pygame.draw.rect(surface, (255, 0, 255), rect, border_radius=8)

        # Draw his speech bubble
        if self.speech_text:
            text = font.render(self.speech_text, True, (0, 0, 0))
            bubble_w = text.get_width() + 20
            bubble_rect = pygame.Rect(self.x - (bubble_w//2), self.y - 65, bubble_w, 30)
            
            pygame.draw.rect(surface, (255, 255, 255), bubble_rect, border_radius=6)
            pygame.draw.rect(surface, (0, 0, 0), bubble_rect, 1, border_radius=6)
            surface.blit(text, text.get_rect(center=bubble_rect.center))
            
def draw_audit_warning(surface, font, owed_taxes, screen_w):
    """Draws the flashing red warning banner."""
    banner_rect = pygame.Rect(0, 50, screen_w, 60)
    pygame.draw.rect(surface, (200, 40, 40), banner_rect)
    pygame.draw.rect(surface, (255, 255, 255), banner_rect, 2)
    
    warn_text = font.render(f"⚠️ IRS AUDIT IN PROGRESS. TAX OWED: ${owed_taxes:,.2f} ⚠️", True, (255, 255, 255))
    surface.blit(warn_text, warn_text.get_rect(center=banner_rect.center))