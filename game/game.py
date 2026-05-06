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
            Stock("AAPL", 150),
            Stock("MSFT", 310),
            Stock("GOOGL", 2800),
            Stock("NVDA", 950),
            Stock("META", 480),
            Stock("NFLX", 620),
        ]

    def add_player(self, name):
        self.players.append(Player(name))

    def update_stocks(self):
        for stock in self.stocks:
            stock.update_price()
