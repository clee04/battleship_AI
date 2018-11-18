from board import Board


class Player(object):
    def __init__(self, name):
        self.name = name
        self.board = Board()

    def message(self, s):
        raise NotImplementedError

    def place_ships(self):
        raise NotImplementedError

    def shoot(self):
        raise NotImplementedError
        
    def game_over(self):
        return self.board.game_over()
