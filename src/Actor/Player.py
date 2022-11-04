from src.Actor.BaseActor import BaseActor
from ..Utils.Enums import BoardTile


class Player(BaseActor):
    def __init__(self, board_tile: BoardTile):
        super().__init__(board_tile)

    def request(self) -> tuple:
        while True:
            try:
                res = input(f"Player {self.board_tile.name}. It's your turn: ")
                parts = res.split(",")
                if len(parts) != 2:
                    raise ValueError()

                x = int(parts[0].strip())
                y = int(parts[1].strip())

                if x < 0 or x >= len(self.board):
                    raise ValueError()
                if y < 0 or y >= len(self.board[x]):
                    raise ValueError()

                return x, y
            except ValueError:
                print(f"You haven't entered a valid x / y coordinate")


class GuiPlayer(BaseActor):
    def __init__(self, board_tile: BoardTile, x, y):
        super().__init__(board_tile)
        self.x = x
        self.y = y

    def request(self) -> tuple:
        return self.x, self.y
