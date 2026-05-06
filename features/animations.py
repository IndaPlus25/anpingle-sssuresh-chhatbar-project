import pygame

def load_8way_animations(base_path):
    directions = ['north', 'south', 'east', 'west', 'northeast', 'northwest', 'southeast', 'southwest']
    animations = {"idle": {}, "walk": {}}

    for d in directions:
        try:
            animations["idle"][d] = pygame.image.load(f"{base_path}/{d}.png").convert_alpha()
        except:
            animations["idle"][d] = None
            
        walk_frames = []
        for i in range(6):
            try:
                img_path = f"{base_path}/walk/walk{d}/f{i}.png"
                img = pygame.image.load(img_path).convert_alpha()
                walk_frames.append(img)
            except:
                break
        animations["walk"][d] = walk_frames
    return animations