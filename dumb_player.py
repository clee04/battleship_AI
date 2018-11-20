from board import SHIPS, Board, InvalidMoveException
from player import Player
import numpy as np


class DumbPlayer(Player):
    def __init__(self, name):
        super(DumbPlayer, self).__init__(name)

    def message(self, s):
        return '[{}]: {}'.format(self.name, s)

    def name(self):
        return self.name

    # Randomly pick locations to place ship
    def place_ships(self):
        for ship in SHIPS.values():
            while True:
                x, y, o = np.random.choice(10), np.random.choice(10), np.random.choice(['h','v'])
                try:
                    self.board.place_ship(x, y, o, ship)
                    break
                except InvalidMoveException:
                    pass

    # Randomly pick locations to shoot
    def shoot(self):
        while True:
            x, y = np.random.choice(10), np.random.choice(10)
            try:
                shot = self.enemy.shoot(x, y)
                print(self.message('Shoot location: ({},{})'.format(x,y)))
                return shot
            except InvalidMoveException:
                pass

