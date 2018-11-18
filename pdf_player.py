from board import SHIPS, Board, InvalidMoveException
from dumb_player import DumbPlayer
import numpy as np


class PDFPlayer(DumbPlayer):
    def __init__(self, name):
        super(DumbPlayer, self).__init__(name)
        self.estimated_board = np.zeros((10, 10))
        self.pdf = {ship: np.zeros((10, 10)) for ship in SHIPS}

    def message(self, s):
        return '[{}]: {}'.format(self.name, s)

    def name(self):
        return self.name

    def update_pdf(self, ship):
        size = SHIPS[ship]
        h_mat = np.zeros((10, 10), dtype=int)
        v_mat = np.zeros((10, 10), dtype=int)
        board = self.estimated_board
        for x in range(10):
            for y in range(11 - size):
                can_be_placed = all(cell in [Board.EMPTY, Board.SHOT_HIT] for cell in board[x,y:y+size])
                if can_be_placed:
                    for z in range(size):
                        h_mat[x,y+z] += 1
        for y in range(10):
            for x in range(11 - size):
                can_be_placed = all(cell in [Board.EMPTY, Board.SHOT_HIT] for cell in board[x:x+size,y])
                if can_be_placed:
                    for z in range(size):
                        v_mat[x+z,y] += 1

        self.pdf[ship] = h_mat + v_mat

    def pick_target(self):
        probs = np.zeros((10,10), dtype=int)
        for ship in SHIPS:
            probs += self.pdf[ship]

        # Pick location based on highest probability
        moves = np.argsort(probs.flatten())[::-1]
        for m in moves:
            x, y = int(m / 10), int(m % 10)
            if self.estimated_board[x,y] not in [Board.SHOT_MISS, Board.SHOT_HIT]:
                return x,y

    def shoot(self):
        # Count how many different orientations a ship can be placed for each cell
        for ship in SHIPS:
            self.update_pdf(ship)

        while True:
            x, y = self.pick_target()
            try:
                shot = self.enemy.shoot(x, y)
                print(self.message('Shoot location: ({},{})'.format(x, y)))
                self.estimated_board[x,y] = shot
                return shot
            except InvalidMoveException:
                raise InvalidMoveException
