# --- Replace features/npc.py with this ---
import pygame
import random
from ui.constants import GAME_W, GAME_H

class EmployeeNPC:
    def __init__(self, x, y, config):
        self.config = config
        self.id = config["id"]
        
        self.x = x
        self.y = y
        self.state = "idle"  # idle, walk, resting
        self.timer = 3000
        
        
        self.max_energy = config["max_energy"]
        self.energy = self.max_energy
        self.speed = 1.5 * config["effectiveness"]
        
        self.direction = "south"
        self.anim_frame = 0
        self.target_x = x
        self.target_y = y

    def update(self, dt):

        if self.state == "resting":
            self.energy += 10 * (dt / 1000) 
            self.anim_frame = 0
            if self.energy >= self.max_energy:
                self.energy = self.max_energy
                self.state = "idle"
                self.timer = 3000
            return 

        # --- MOVEMENT LOGIC ---
        if self.state == "idle":
            self.timer -= dt
            self.anim_frame = 0
            if self.timer <= 0:
                self.state = "walk"
                self.target_x = random.randint(100, GAME_W - 100)
                self.target_y = random.randint(100, GAME_H - 100)
                
        elif self.state == "walk":
            self.energy -= 5 * (dt / 1000) 
            if self.energy <= 0:
                self.energy = 0
                self.state = "resting"
                return

            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = (dx**2 + dy**2)**0.5

            if dist < 5: 
                self.state = "idle"
                self.timer = 3000  
            else:
                move_x = (dx / dist) * self.speed
                move_y = (dy / dist) * self.speed
                self.x += move_x
                self.y += move_y

                dir_str = ""
                if move_y < -0.5: dir_str += "north"
                elif move_y > 0.5: dir_str += "south"
                if move_x < -0.5: dir_str += "west"
                elif move_x > 0.5: dir_str += "east"
                
                if dir_str: self.direction = dir_str
                self.anim_frame = (self.anim_frame + 0.1) % 6

    def draw(self, surface, anims):
        rect = pygame.Rect(self.x, self.y, 92, 92) 
        d = self.direction
        
        if self.state == "walk" and anims["walk"].get(d):
            img = anims["walk"][d][int(self.anim_frame)]
        else:
            #sleep
            img = anims["idle"].get(d)
            
        if img:
            img = pygame.transform.scale(img, (92, 92))
            surface.blit(img, rect)