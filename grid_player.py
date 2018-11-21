from board import SHIPS, Board, InvalidMoveException
from dumb_player import DumbPlayer
import numpy as np


class GridPlayer(DumbPlayer):
    def __init__(self, name):
        super(GridPlayer, self).__init__(name)
        self.estimated_board = np.zeros((10,10))

    def message(self, s):
        return '[{}]: {}'.format(self.name, s)

    def name(self):
        return self.name

    # Prioritize picking neighboring cells of a hit location
    def pick_target(self):
        hits = np.argwhere(self.estimated_board==Board.SHOT_HIT)
        for (i,j) in hits:
            if i > 0 and self.estimated_board[i-1,j] == 0:
                return i-1, j
            if j > 0 and self.estimated_board[i,j-1] == 0:
                return i, j-1
            if i < 9 and self.estimated_board[i+1,j] == 0:
                return i+1, j
            if j < 9 and self.estimated_board[i,j+1] == 0:
                return i, j+1
            
        new_spots = np.argwhere(self.estimated_board==0)
        return new_spots[np.random.choice(len(new_spots))]

    def shoot(self):
        while True:
            x, y = self.pick_target()
            try:
                shot = self.enemy.shoot(x, y)
                self.estimated_board[x,y] = shot
                # print(self.message('Shoot location: ({},{})'.format(x,y)))
                return shot
            except InvalidMoveException:
                pass

    def reset(self):
        self.board = Board()
        self.estimated_board = np.zeros((10,10))