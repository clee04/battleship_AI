from board import Board
from human_player import HumanPlayer
from dumb_player import DumbPlayer
from grid_player import GridPlayer
from pdf_player import PDFPlayer
from time import time
import numpy as np
import cProfile, pstats, io

class Simulation:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def run(self):
        # Place ships
        self.p1.place_ships()
        board = self.p2.place_ships().copy()

        # Continue shooting till all ships are destroyed
        moves = 0
        while True:
            moves += 1
            if self.p1.shoot() == Board.SHOT_HIT:
                if self.p2.game_over():
                    break

        return board, moves

def generate_train_batch(batch_size, player):
    # Train set
    boards = np.zeros((batch_size,10,10),dtype=np.float32)
    moves = np.zeros((batch_size),dtype=np.float32)

    # Initialize players
    if player == 1:
        p1 = DumbPlayer('p1')
    elif player == 2:
        p1 = GridPlayer('p1')
    else:
        p1 = PDFPlayer('p1')
    p2 = DumbPlayer('p2')

    # Initialize Game and run
    # Counts how many shoots a player needs to finish
    for r in range(batch_size):
        p1.reset()
        p2.reset()
        p1.enemy = p2.board
        p2.enemy = p1.board
        game = Simulation(p1, p2)
        boards[r], moves[r] = game.run()

    return np.reshape(boards, (batch_size,10,10,1)), np.reshape(moves, (batch_size,1))
    
def generate_test_batch(batch_size, player):
    boards = np.zeros((batch_size,10,10),dtype=np.float32)
    moves = np.zeros((batch_size),dtype=np.float32)
    p1 = DumbPlayer('p1')
    
    for r in range(batch_size):
        p1.reset()
        boards[r] = p1.place_ships()

    return np.reshape(boards, (batch_size,10,10,1)), np.reshape(moves, (batch_size,1))    
