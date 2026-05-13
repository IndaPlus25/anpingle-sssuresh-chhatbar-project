import pygame
import random
from ui.constants import GAME_W, GAME_H, GAME_MINUTE_MS
from features.collision import move_with_collision
from ui.screens import draw_sleep_bubble

class EmployeeNPC:
    def __init__(self, x, y, config):
        self.config = config
        self.id = config["id"]
        
        self.x = x
        self.y = y
        self.state = "idle"  # idle, walk, resting
    
        self.timer_minutes = 15.0 
        
        self.max_energy = config["max_energy"]
        self.energy = self.max_energy
        self.speed = 1.5 * config["effectiveness"]
        
        self.direction = "south"
        self.anim_frame = 0
        self.target_x = x
        self.target_y = y

    def update(self, dt, assets):
        game_minutes_passed = dt / GAME_MINUTE_MS 

        if self.state == "resting":
            self.energy += 1.5 * game_minutes_passed 
            self.anim_frame = 0
            if self.energy >= self.max_energy:
                self.energy = self.max_energy
                self.state = "idle"
                self.timer_minutes = 15.0 # Idle for 15 game minutes after resting
            return 

        if self.state == "idle":
            self.timer_minutes -= game_minutes_passed
            self.anim_frame = 0
            if self.timer_minutes <= 0:
                self.state = "walk"
                self.target_x = random.randint(100, GAME_W - 100)
                self.target_y = random.randint(100, GAME_H - 100)
                
        elif self.state == "walk":
            # Drain 1 energy per in-game minute
            self.energy -= 2.0 * game_minutes_passed 
            if self.energy <= 0:
                self.energy = 0
                self.state = "resting"
                return

            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = (dx**2 + dy**2)**0.5

            if dist < 5: 
                self.state = "idle"
                self.timer_minutes = random.uniform(10.0, 30.0) # Idle for 10-30 game minutes
            else:
                move_x = (dx / dist) * self.speed
                move_y = (dy / dist) * self.speed
                
                old_x = self.x
                old_y = self.y
                
                move_with_collision(
                    self, move_x, move_y, 
                    assets["walls_mask"], 
                    assets["feet_mask"], 
                    props_collision=assets.get("props_collision", []), 
                    char_width=92, char_height=92, 
                    custom_offset_x=30, custom_offset_y=76 
                )

                # Bump Detection
                if abs(self.x - old_x) < 0.5 and abs(self.y - old_y) < 0.5:
                    self.target_x = random.randint(100, GAME_W - 100)
                    self.target_y = random.randint(100, GAME_H - 100)
                    self.state = "idle" 
                    self.timer_minutes = 5.0 # Pause for 5 game minutes when bumping into a wall

                # Determine direction for animation
                dir_str = ""
                if move_y < -0.5: dir_str += "north"
                elif move_y > 0.5: dir_str += "south"
                if move_x < -0.5: dir_str += "west"
                elif move_x > 0.5: dir_str += "east"
                
                if dir_str: self.direction = dir_str
                self.anim_frame = (self.anim_frame + 0.1) % 6

    def draw(self, surface, anims, small_font):
        rect = pygame.Rect(self.x, self.y, 92, 92) 
        d = self.direction
        
        if self.state == "walk" and anims["walk"].get(d):
            img = anims["walk"][d][int(self.anim_frame)]
        else:
            img = anims["idle"].get(d)
            
        if img:
            img = pygame.transform.scale(img, (92, 92))
            surface.blit(img, rect)
            
        # Draw the Zzz bubble if resting
        if self.state == "resting":
            draw_sleep_bubble(surface, self.x + 60, self.y - 10, small_font)