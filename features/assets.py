import pygame
from ui.constants import GAME_W, GAME_H, CHARACTERS, MAP_PROPS, SHOP_ITEMS
from features.animations import load_8way_animations

def load_all_assets():
    """Loads fonts, images, backgrounds, and animations. Returns a dictionary."""
    assets = {}
    
    # Fonts
    font_path = "ui/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf"
    assets["title_font"] = pygame.font.Font(font_path, 64)
    assets["body_font"]  = pygame.font.Font(font_path, 36)
    assets["small_font"] = pygame.font.Font(font_path, 24)
    assets["hud_font"]   = pygame.font.Font(font_path, 32)

    #Backgrounds
    try: 
        bg = pygame.image.load("ui/backgrounds/office_bg_plain.png").convert()
        assets["bg"] = pygame.transform.scale(bg, (GAME_W, GAME_H))
    except: 
        assets["bg"] = pygame.Surface((GAME_W, GAME_H))
        assets["bg"].fill((30, 40, 60))

    assets["desks"] = {}
    for item in SHOP_ITEMS:
        try:
            img = pygame.image.load(item["file"]).convert_alpha()
            assets["desks"][item["id"]] = pygame.transform.scale(img, (180, 140))
        except:
            print(f"Warning: Could not load {item['file']}")
            assets["desks"][item["id"]] = None
            
    # Default equipped desk
    assets["current_desk_id"] = "desk1" 
    assets["desk_rect"] = pygame.Rect(580, 320, 180, 140)
    assets["computer_rect"] = pygame.Rect(580 + 40, 320 + 40, 100, 40)

    assets["props"]={}
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



    # Characters and animations
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

    # 4. Icons
    try:
        assets["icon_coin"] = pygame.transform.scale(pygame.image.load("ui/assets/coin.png").convert_alpha(), (36, 36))
        assets["icon_play"] = pygame.transform.scale(pygame.image.load("ui/assets/play.png").convert_alpha(), (28, 28))
        assets["icon_person"] = pygame.transform.scale(pygame.image.load("ui/assets/person.png").convert_alpha(), (28, 28))
        assets["icon_quit"] = pygame.transform.scale(pygame.image.load("ui/assets/quit.png").convert_alpha(), (28, 28))
    except: 
        assets["icon_coin"] = assets["icon_play"] = assets["icon_person"] = assets["icon_quit"] = None

    return assets