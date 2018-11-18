from board import SHIPS, Board, InvalidMoveException
from player import Player
import numpy as np
import sys

class HumanPlayer(Player):
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)
        self.shot_record = np.zeros((10,10))

    def message(self, s):
        return '[{}]: {}'.format(self.name, s)

    def name(self):
        return self.name

    def place_ships(self):
        for ship in SHIPS.values():
            while True:
                try:
                    x, y, o = input(self.message('Pick upper-left position and orientation (row, col, v or h): ')).replace(" ","").split(',')
                    x, y = int(x), int(y)
                    self.board.place_ship(x, y, o, ship)
                    self.board.print_board()
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
