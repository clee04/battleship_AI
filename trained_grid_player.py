from board import SHIPS, Board, InvalidMoveException
from grid_player import GridPlayer
import numpy as np


class TrainedGridPlayer(GridPlayer):
    def __init__(self, name):
        super(TrainedGridPlayer, self).__init__(name)
        self.estimated_board = np.zeros((10,10))
        print(np.load('./board_2.npy')[:,:,0])        

    def message(self, s):
        return '[{}]: {}'.format(self.name, s)

    def name(self):
        return self.name

    def place_ships(self):
        self.board.board = np.load('./board_2.npy')[:,:,0]
        # self.board.print_board()
