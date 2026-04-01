from .player import Player

class Game:
    def __init__(self):
        self.players = []

    def add_player(self, name):
        self.players.append(Player(name))