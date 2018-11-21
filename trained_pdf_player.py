from board import SHIPS, Board, InvalidMoveException
from pdf_player import PDFPlayer
import numpy as np


class TrainedPDFPlayer(PDFPlayer):
    def __init__(self, name):
        super(TrainedPDFPlayer, self).__init__(name)
        self.estimated_board = np.zeros((10,10))
        print(np.load('./board_3.npy')[:,:,0])        

    def message(self, s):
        return '[{}]: {}'.format(self.name, s)

    def name(self):
        return self.name

    def place_ships(self):
        self.board.board = np.load('./board_3.npy')[:,:,0]
        # self.board.print_board()
