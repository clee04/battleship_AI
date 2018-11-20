from board import SHIPS, Board, InvalidMoveException
from dumb_player import DumbPlayer
import numpy as np


class PDFPlayer(DumbPlayer):
    def __init__(self, name):
        super(DumbPlayer, self).__init__(name)
        self.estimated_board = np.zeros((10, 10))
        self.initialize_pdf()

    def message(self, s):
        return '[{}]: {}'.format(self.name, s)

    def name(self):
        return self.name

    def initialize_pdf(self):
        sizes = SHIPS.values()
        board = self.estimated_board
        self.pdf = np.zeros((10,10))

        # Could be optimize
        for size in sizes:
            z = size
            for x in range(10):
                for y in range(11 - size):
                    can_be_placed_h = all(np.logical_or(board[x,y:y+size] == Board.EMPTY, board[x,y:y+size] == Board.SHOT_HIT))
                    can_be_placed_v = all(np.logical_or(board[y:y+size,x] == Board.EMPTY, board[y:y+size,x] == Board.SHOT_HIT))
                    if can_be_placed_h:
                        self.pdf[x,y:y+z] += 1
                    if can_be_placed_v:
                        self.pdf[y:y+z,x] += 1


    def update_pdf(self,x_miss,y_miss):
        board = self.estimated_board
        sizes = SHIPS.values()

        for size in sizes:
            for x in range(max(0, x_miss - size + 1), min(x_miss + 1, 11 - size)):
                can_be_placed_v = all(np.logical_or(board[x:x+size,y_miss] == Board.EMPTY, board[x:x+size,y_miss] == Board.SHOT_HIT))
                if can_be_placed_v:
                        self.pdf[x:x+size,y_miss] -= 1

            for y in range(max(0, y_miss - size + 1), min(y_miss + 1, 11 - size)):
                can_be_placed_h = all(np.logical_or(board[x_miss,y:y+size] == Board.EMPTY, board[x_miss,y:y+size] == Board.SHOT_HIT))
                if can_be_placed_h:
                    self.pdf[x_miss,y:y+size] -= 1


    def pick_target(self):
        # Pick location based on highest probability
        moves = np.argsort(self.pdf.flatten())[::-1]
        for m in moves:
            x, y = int(m / 10), int(m % 10)
            if self.estimated_board[x,y] not in [Board.SHOT_MISS, Board.SHOT_HIT]:
                return x,y

    def shoot(self):
        # Count how many different orientations a ship can be placed for each cell
        while True:
            x, y = self.pick_target()
            try:
                shot = self.enemy.shoot(x, y)
                print(self.message('Shoot location: ({},{})'.format(x, y)))
                if shot == Board.SHOT_MISS:
                    self.update_pdf(x,y)
                self.estimated_board[x,y] = shot
                return shot
            except InvalidMoveException:
                raise InvalidMoveException

    def reset(self):
        self.board = Board()
        self.estimated_board = np.zeros((10, 10))
        self.initialize_pdf()
        
