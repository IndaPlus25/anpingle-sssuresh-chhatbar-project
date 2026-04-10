import random

class Stock:
    def __init__(self, name, price):
        self.name = name
        self.price = float(price)

    def update_price(self):
        change = random.uniform(-10.0, 10.0)
        self.price += change
        self.price = max(0.01, self.price)
        self.price = round(self.price, 2)
