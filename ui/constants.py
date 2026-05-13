import pygame

# Screen Settings
GAME_W, GAME_H = 1280, 720

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (255, 0,   0)
GREEN  = (0,   200, 100)
BLUE   = (50,  130, 255)
DARK   = (15,  15,  30)
PANEL  = (25,  25,  50)
GOLD   = (255, 210, 60)
GRAY   = (140, 140, 160)
LGRAY  = (200, 200, 220)

# Character Definitions
CHARACTERS = [
    {"name": "Alex",   "file": "ui/characters/char1.png", "desc": "Balanced trader"},
    {"name": "Morgan", "file": "ui/characters/char2.png", "desc": "Risk taker"},
    {"name": "Jordan", "file": "ui/characters/char3.png", "desc": "Market analyst"},
]

# shop
SHOP_ITEMS = [
    {"id": "desk1", "name": "Basic Desk",      "price": 0,    "file": "ui/assets/desks/desk1.png","category": "Desks"},
    {"id": "desk2", "name": "Standard Desk",   "price": 5000,  "file": "ui/assets/desks/desk2.png","category": "Desks"},
    {"id": "desk3", "name": "Executive Desk",  "price": 12000, "file": "ui/assets/desks/desk3.png","category": "Desks"},
    {"id": "desk4", "name": "Trading Station", "price": 25000, "file": "ui/assets/desks/desk4.png","category": "Desks"},
    {"id": "desk5", "name": "Hedge Fund Rig",  "price": 50000, "file": "ui/assets/desks/desk5.png","category": "Desks"},
    {"id": "wall1", "name": "Basic Brick",  "price": 0, "file": "ui/backgrounds/walls/walls_01.png","category": "Walls"},
    {"id": "wall2", "name": "Industrial Plating",  "price": 50000, "file": "ui/backgrounds/walls/walls_02.png","category": "Walls"},
    {"id": "wall3", "name": "Refurbished Steel",  "price": 100000, "file": "ui/backgrounds/walls/walls_03.png","category": "Walls"},
    {"id": "wall4", "name": "Modern Corporate",  "price": 500000, "file": "ui/backgrounds/walls/walls_04.png","category": "Walls"},
    {"id": "wall5", "name": "Cyber Grid",  "price": 1000000, "file": "ui/backgrounds/walls/walls_05.png","category": "Walls"},
]

# map assets
MAP_PROPS = [
    {"type": "water", "x": 355, "y": 70},
    {"type": "locker_03", "x": 673, "y": 75},
    {"type": "locker_02", "x": 981, "y": 315},
    {"type": "table_01", "x": 300, "y": 400}, 
    {"type": "shopdesk", "x": 50, "y": 120}, 
    {"type": "box_01", "x": 60, "y": 430}, 
    {"type": "box_02", "x": 350, "y": 600}, 
]