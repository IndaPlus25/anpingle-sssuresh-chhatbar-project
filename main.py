from game.game import Game
from ui.pygame import run

game = Game()
game.add_player("Alice")

run(game)