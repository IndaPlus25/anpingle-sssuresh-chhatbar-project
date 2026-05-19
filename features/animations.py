import pygame,os,json

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

def load_json_animations(base_path):
    json_path = os.path.join(base_path, "metadata.json")
    animations = {"idle": {}, "walk": {}}
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON at {json_path}: {e}")
        return animations

    def format_dir(d):
        return d.replace("-", "")

    rotations = data.get("frames", {}).get("rotations", {})
    for d, path in rotations.items():
        full_path = os.path.join(base_path, path)
        try:
            img = pygame.image.load(full_path).convert_alpha()
            animations["idle"][format_dir(d)] = img
        except:
            print(f"Warning: Could not load {full_path}")

    walks = data.get("frames", {}).get("animations", {}).get("animation-walk", {})
    for d, paths in walks.items():
        frames = []
        for path in paths:
            full_path = os.path.join(base_path, path)
            try:
                img = pygame.image.load(full_path).convert_alpha()
                frames.append(img)
            except:
                print(f"Warning: Could not load {full_path}")
        animations["walk"][format_dir(d)] = frames

    return animations