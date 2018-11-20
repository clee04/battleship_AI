from board import SHIPS, Board, InvalidMoveException
from player import Player
import numpy as np
import sys

class HumanPlayer(Player):
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)
        self.shot_record = np.zeros((10,10))
        self.visualize()

    def message(self, s):
        return '[{}]: {}'.format(self.name, s)

    def name(self):
        return self.name

    def visualize(self):
        import matplotlib.pyplot as plt
        plt.ion()
        self.fig = plt.figure(figsize=(8,4))
        self.ax = self.fig.add_subplot(121)
        self.ax.set_title('Place your ships!')
        self.ax.set_xticks(np.arange(10))
        self.ax.set_yticks(np.arange(10))
        
        self.ax2 = self.fig.add_subplot(122)
        self.ax2.set_title('Shoot your enemy ships!')
        self.ax2.set_xticks(np.arange(10))
        self.ax2.set_yticks(np.arange(10))

        self.ax.imshow(self.board.board, aspect='auto')
        self.ax2.imshow(self.shot_record, aspect='auto')

    def place_ships(self):
        # Visualization for placing your ship
        for ship in SHIPS.values():
            while True:
                try:
                    x, y, o = input(self.message('Pick upper-left position and orientation (row, col, v or h): ')).replace(" ","").split(',')
                    x, y = int(x), int(y)
                    self.board.place_ship(x, y, o, ship)
                    self.board.print_board()
                    self.ax.imshow(self.board.board)
                    break
                except KeyboardInterrupt:
                    print('\nQuitting game...')
                    sys.exit(0)
                except InvalidMoveException:
                    print('Invalid Move. Try another!')
                except:
                    print('You need to enter in the form of (row,col,v/h)')
                    print('For example: 2,5,v\n')

    def shoot(self):
        while True:
            try:
                x, y = input(self.message('Pick shoot location (row,col): ')).split(',')
                x, y = int(x), int(y)
                shot = self.enemy.shoot(x, y)
                self.shot_record[x,y] = shot
                self.ax2.imshow(self.shot_record)
                break
            except KeyboardInterrupt:
                print('\nQuitting game...')
                sys.exit(0)
            except InvalidMoveException:
                print('Invalid Move. Try another!\n')
            except:
                print('You need to enter in the form of (row,col)')
                print('For example: 2,5\n')

        print(self.message('1 indicates miss; 6 indicates hit'))
        print(np.array(self.shot_record))
        return shot

    def reset(self):
        self.board = Board()
        self.shot_record = np.zeros((10,10))
