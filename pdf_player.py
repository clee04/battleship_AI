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
        self.pdf[ship] = np.zeros((10,10))
        board = self.estimated_board

        temp = np.zeros((10, 11-size))
        np.argwhere(temp)


        for x in range(10):
            for y in range(11 - size):
                can_be_placed_h = np.logical_or(board[x,y:y+size] == Board.EMPTY, board[x,y:y+size] == Board.SHOT_HIT)
                can_be_placed_v = all(cell in [Board.EMPTY, Board.SHOT_HIT] for cell in board[y:y+size,x])
                if can_be_placed_h:
                    self.pdf[ship][x,y:y+z] += 1
                if can_be_placed_v:
                    self.pdf[ship][y:y+z,x] += 1

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
                print(self.estimated_board)
                return shot
            except InvalidMoveException:
                raise InvalidMoveException

    def reset(self):
        self.board = Board()
        self.estimated_board = np.zeros((10, 10))
        self.pdf = {ship: np.zeros((10, 10)) for ship in SHIPS}
