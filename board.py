import numpy as np

class InvalidMoveException(Exception):
    pass

# Types of ships and lengths
SHIPS = {'DESTROYER': 2,
         'SUBMARINE': 3,
         'CRUISER': 3,
         'BATTLESHIP': 4,
         'CARRIER': 5}

class Board:
    EMPTY      = 0
    SHOT_MISS  = 1
    SHOT_HIT   = 6

    def __init__(self, size=10):
        self.size = size
        self.board = np.zeros((size,size))

    def validate(self, x, y, orientation, ship):
        ship_end = (y if orientation == 'h' else x) + ship
        if ship_end > self.size:
            raise InvalidMoveException

        if orientation == 'h':
            for y0 in range(y, ship_end):
                if self.board[x,y0] != Board.EMPTY:
                    raise InvalidMoveException
        else:
            for x0 in range(x, ship_end):
                if self.board[x0,y] != Board.EMPTY:
                    raise InvalidMoveException

    def place_ship(self, x, y, orientation, ship):
        try:
            self.validate(x, y, orientation, ship)
        except InvalidMoveException:
            raise InvalidMoveException

        ship_end = (y if orientation == 'h' else x) + ship
        if orientation == 'h':
            for y0 in range(y, ship_end):
                self.board[x,y0] = ship
        else:
            for x0 in range(x, ship_end):
                self.board[x0,y] = ship

    def shoot(self, x, y):
        # Invalid position if already shot
        while True:
            if x >= self.size or y >= self.size or x < 0 or y < 0 or \
               self.board[x,y] in [Board.SHOT_HIT, Board.SHOT_MISS]:
                raise InvalidMoveException
            else:
                break
        
        # Mark shot hit or miss and return the value
        self.board[x,y] = Board.SHOT_MISS if self.board[x,y] == Board.EMPTY else Board.SHOT_HIT
        return self.board[x,y]

    def print_board(self):
        print(self.board)
        print()

    def game_over(self):
        # Game over if there are no ships left on the board
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x,y] in SHIPS.values():
                    return False

        return True
