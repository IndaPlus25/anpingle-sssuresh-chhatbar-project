class Player:
    def __init__(self, name):
        self.name = name
        self.cash = 1000000
        self.portfolio = {}
        self.x = 300
        self.y = 200
        self.direction = "south"
        self.is_moving = False

    def move(self, dx, dy, max_w, max_h):
        if dx != 0 or dy != 0:
            self.is_moving = True
            self.x += dx
            self.y += dy
            
            self.x = max(0, min(self.x, max_w - 40))
            self.y = max(0, min(self.y, max_h - 40))
            
            
            dirs = []
            if dy < 0: dirs.append("north")
            elif dy > 0: dirs.append("south")
            if dx > 0: dirs.append("east")
            elif dx < 0: dirs.append("west")
            self.direction = "".join(dirs)
        else:
            self.is_moving = False