from .player import Player
from .stock import Stock

class Game:
    def __init__(self):
        self.players = []
        self.stocks = [
            Stock("AMZN", 120),
            Stock("TSLA", 85),
            Stock("FAILS", 205),
            Stock("ASML", 47),
        ]

    def add_player(self, name):
        self.players.append(Player(name))