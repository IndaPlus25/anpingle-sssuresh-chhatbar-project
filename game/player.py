class Player:
    def __init__(self, name):
        self.name = name
        self.cash = 1000000
        self.portfolio = {}
        self.x = 300
        self.y = 200

    def move(self, dx):
        self.x += dx
        self.x = max(0, min(self.x, 600 - 40))

