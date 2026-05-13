import pygame
from ui.constants import GAME_W, GAME_H, CHARACTERS, MAP_PROPS, SHOP_ITEMS, AVAILABLE_EMPLOYEES
from features.animations import load_8way_animations, load_json_animations

def load_all_assets():
    """Loads fonts, images, backgrounds, and animations. Returns a dictionary."""
    assets = {}
    
    # Fonts
    pixelify_path = "ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf"
    monogram_path = "ui/fonts/monogram/ttf/monogram.ttf"
    # font_path = "ui/fonts/pixellari/Pixellari.ttf"
    # font_path = "ui/fonts/m5x7.ttf"
    # font_path = "ui/fonts/thaleahfat/ThaleahFat.ttf"
    assets["title_font"] = pygame.font.Font(pixelify_path, 64)
    assets["body_font"]  = pygame.font.Font(pixelify_path, 36)
    assets["hud_bold_font"] = pygame.font.Font(pixelify_path, 24)
    assets["small_font"] = pygame.font.Font(monogram_path, 24)
    assets["hud_font"]   = pygame.font.Font(monogram_path, 32)

    #Backgrounds
    try: 
        bg = pygame.image.load("ui/backgrounds/office_bg_plain2.png").convert()
        assets["bg"] = pygame.transform.scale(bg, (GAME_W, GAME_H))
    except: 
        assets["bg"] = pygame.Surface((GAME_W, GAME_H))
        assets["bg"].fill((30, 40, 60))

    assets["desks"] = {}
    assets["wall_images"] = {}
    assets["wall_masks"] = {} 
    assets["shop_thumbnails"] = {}
    
    for item in SHOP_ITEMS:
        try:
            img = pygame.image.load(item["file"]).convert_alpha()
            # Thumbnail for shop UI
            assets["shop_thumbnails"][item["id"]] = pygame.transform.scale(img, (75, 55))
            
            # Sort by category
            cat = item.get("category", "Desks")
            if cat == "Desks":
                assets["desks"][item["id"]] = pygame.transform.scale(img, (180, 140))
            elif cat == "Walls":
                scaled_wall = pygame.transform.scale(img, (GAME_W, GAME_H))
                assets["wall_images"][item["id"]] = scaled_wall
                assets["wall_masks"][item["id"]] = pygame.mask.from_surface(scaled_wall)
        except Exception as e:
            print(f"Warning: Could not load {item.get('file', 'Unknown')}: {e}")
            
    
    assets["current_desk_id"] = "desk1" 
    assets["desk_rect"] = pygame.Rect(580, 320, 180, 140)
    assets["computer_rect"] = pygame.Rect(580 + 40, 320 + 40, 100, 40)

    # --- CRITICAL FIX: Ensure walls_mask exists immediately ---
    assets["current_wall_id"] = "wall1"
    if "wall1" in assets["wall_masks"]:
        assets["walls_mask"] = assets["wall_masks"]["wall1"]
    else:
        try:
            walls_img = pygame.image.load("ui/backgrounds/walls/walls_05.png").convert_alpha()
            walls_img = pygame.transform.scale(walls_img, (GAME_W, GAME_H))
            assets["wall_images"]["fallback"] = walls_img
            assets["walls_mask"] = pygame.mask.from_surface(walls_img)
            assets["current_wall_id"] = "fallback"
        except Exception as e:
            print(f"Error loading fallback walls: {e}")
            assets["walls_mask"] = pygame.mask.Mask((GAME_W, GAME_H)) 

    assets["props"] = {}

    try:
        assets["props"]["water"]=pygame.image.load("ui/assets/water.png")
        assets["props"]["table_01"]=pygame.image.load("ui/assets/table_01.png")
        assets["props"]["locker_02"]=pygame.image.load("ui/assets/locker_02.png")
        assets["props"]["locker_03"]=pygame.image.load("ui/assets/locker_03.png")
        assets["props"]["shopdesk"]=pygame.image.load("ui/assets/shopdesk.png")
        assets["props"]["box_01"]=pygame.image.load("ui/assets/box_01.png")
        assets["props"]["box_02"]=pygame.image.load("ui/assets/box_02.png")

        assets["props"]["water"] = pygame.transform.scale(assets["props"]["water"], (34, 94))        
        assets["props"]["table_01"] = pygame.transform.scale(assets["props"]["table_01"], (115, 81))        
        assets["props"]["locker_02"] = pygame.transform.scale(assets["props"]["locker_02"], (124, 81))        
        assets["props"]["locker_03"] = pygame.transform.scale(assets["props"]["locker_03"], (124, 81))        
        assets["props"]["shopdesk"] = pygame.transform.scale(assets["props"]["shopdesk"], (150, 81))        
        assets["props"]["box_01"] = pygame.transform.scale(assets["props"]["box_01"], (40, 40))        
        assets["props"]["box_02"] = pygame.transform.scale(assets["props"]["box_02"], (40, 40))        
    except Exception as e:
        print(f"Warning couldnt load props:{e}")

    char_images = []
    for c in CHARACTERS:
        try: char_images.append(pygame.image.load(c["file"]).convert_alpha())
        except: char_images.append(None)
    assets["char_images"] = char_images

    assets["all_char_anims"] = [
        load_8way_animations("ui/characters/char1"),
        load_8way_animations("ui/characters/char2"),
        load_8way_animations("ui/characters/char3")
    ]

    assets["staff_anims"] = {}
    assets["staff_portraits"] = {}
    
    for emp in AVAILABLE_EMPLOYEES:
        assets["staff_anims"][emp["id"]] = load_json_animations(emp["folder"])
        
        try:
            port = pygame.image.load(emp["portrait"]).convert_alpha()
            assets["staff_portraits"][emp["id"]] = pygame.transform.scale(port, (40, 40))
        except:
            assets["staff_portraits"][emp["id"]] = None

    # 4. Icons
    try:
        assets["icon_coin"] = pygame.transform.scale(pygame.image.load("ui/assets/coin.png").convert_alpha(), (36, 36))
        assets["icon_play"] = pygame.transform.scale(pygame.image.load("ui/assets/play.png").convert_alpha(), (28, 28))
        assets["icon_person"] = pygame.transform.scale(pygame.image.load("ui/assets/person.png").convert_alpha(), (28, 28))
        assets["icon_quit"] = pygame.transform.scale(pygame.image.load("ui/assets/quit.png").convert_alpha(), (28, 28))
    except: 
        assets["icon_coin"] = assets["icon_play"] = assets["icon_person"] = assets["icon_quit"] = None

    FEET_W, FEET_H = 32, 16 
    feet_surface = pygame.Surface((FEET_W, FEET_H), pygame.SRCALPHA)
    feet_surface.fill((255, 255, 255, 255)) # Solid white
    assets["feet_mask"] = pygame.mask.from_surface(feet_surface)

    assets["props_collision"] = []
    from ui.constants import MAP_PROPS
    for prop in MAP_PROPS:
        img = assets["props"].get(prop["type"])
        if img:
            p_mask = pygame.mask.from_surface(img)
            assets["props_collision"].append({
                "mask": p_mask,
                "x": prop["x"],
                "y": prop["y"]
            })
            
    return assets