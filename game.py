from board import Board
from human_player import HumanPlayer
from dumb_player import DumbPlayer
from grid_player import GridPlayer
from pdf_player import PDFPlayer
from time import time
import cProfile, pstats, io
# from pstats import SortKey


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def game_over(self):
        return self.p1.game_over() or self.p2.game_over()

    def run(self):
        # Place ships
        self.p1.place_ships()
        print('Placed p1 ships.')
        self.p2.place_ships()
        print('Placed p2 ships.')

        # Continue shooting till all ships are destroyed
        p1_hits = 0
        p2_hits = 0
        while True:
            if self.p1.shoot() == Board.SHOT_HIT:
                p1_hits += 1
                print(self.p1.message('Hit! {} ship locations hit so far.\n'.format(p1_hits)))
                if self.p1.game_over():
                    print('\n\nGame Over. All of your ships were destroyed...!')
                    winner = 0
                    break
            else:
                print(self.p1.message('Miss...\n'))
            if self.p2.shoot() == Board.SHOT_HIT:
                p2_hits += 1
                print(self.p2.message('Hit! {} ship locations hit so far.\n').format(p2_hits))
                if self.p2.game_over():
                    print('\n\nGood job! You won!!')
                    winner = 1
                    break
            else:
                print(self.p2.message('Miss...\n'))

        # Show board at the end of the game
        print(self.p1.message('Board'))
        self.p1.board.print_board()
        print(self.p2.message('Board'))
        self.p2.board.print_board()

        return winner

    def print_instruction(self):
        print("\nThe goal of this game is to destroy all enemy's ships.")
        print("First pick 5 locations on a 10x10 grid to place your ships.")
        print("Then try to shoot all enemy ships before they destroy yours!")
        print("Remember, the enemy ships can be anywhere on the grid!")
        print("The grid size is 10x10! Good luck!\n")


if __name__ == '__main__':
    print('\nWelcome to the Battleship!')
    level = 3#int(input('Please select a level (1,2,3): '))
    rounds = 100

    # Initialize players
    p1 = GridPlayer('p1')
    if level == 1:
        p2 = DumbPlayer('p2')
    elif level == 2:
        p2 = GridPlayer('p2')
    else:
        p2 = PDFPlayer('p2')

    # Initialize Game and run
    # Score counts how many times player1 wins
    pr = cProfile.Profile()
    pr.enable()
    start_time = time()
    score = 0
    for _ in range(rounds):
        p1.reset()
        p2.reset()
        p1.enemy = p2.board
        p2.enemy = p1.board
        game = Game(p1, p2)
        game.print_instruction()
        score += game.run()
    end_time = time()
    print("Run time: {}".format(end_time - start_time))
    pr.disable()
    s = io.StringIO()
    # sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    print(s.getvalue())

    score /= rounds
    score *= 100
    print('Player1 won {}% of the rounds'.format(score))
    