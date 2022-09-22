from abc import abstractmethod

from ..Utils.Enums import BoardTile


class BaseActor:
    def __init__(self, board_tile: BoardTile):
        self.board_tile = board_tile
        self.board = ()

    def initialize_game(self, board):
        self.board = board

    @abstractmethod
    def request(self) -> tuple:
        raise Exception("The request method hasn't been implemented yet")
