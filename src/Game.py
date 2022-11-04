from src.Utils.Enums import *
from src.Utils.Exceptions import *
from src.Actor.BaseActor import BaseActor

MAPPINGS = {
    BoardTile.EMPTY.value: " ",
    BoardTile.CROSS.value: "x",
    BoardTile.CIRCLE.value: "o"
}


class GameEnv:
    def __init__(self, first_stepper, second_stepper):
        self.board = ()
        self.reset_board()

        self.first_stepper = first_stepper
        if self.first_stepper is not None:
            self.first_stepper.initialize_game(self.board)

        self.second_stepper = second_stepper
        if self.second_stepper is not None:
            self.second_stepper.initialize_game(self.board)

    def reset_board(self):
        self.board = ([BoardTile.EMPTY, BoardTile.EMPTY, BoardTile.EMPTY],
                      [BoardTile.EMPTY, BoardTile.EMPTY, BoardTile.EMPTY],
                      [BoardTile.EMPTY, BoardTile.EMPTY, BoardTile.EMPTY])

    def receive_formatted_board(self):
        board = ""
        for row in self.board:
            for item in row:
                board += MAPPINGS[item.value] + " "
            board += "\n"

        return board

    def get_stepper(self, step: int):
        return self.second_stepper if step % 2 == 1 else self.first_stepper

    def next_step(self, stepper: BaseActor):
        x, y = stepper.request()

        board_state = self.board[x][y]
        if board_state != BoardTile.EMPTY:
            raise TileTakenException()

        self.board[x][y] = stepper.board_tile

    def check_game_state(self, board_tile: BoardTile) -> GameState:
        length = len(self.board)

        # Check rows
        for row in self.board:
            if check_list(row, board_tile):
                return GameState.WON

        # Check column
        for i in range(length):
            if check_list([self.board[j][i] for j in range(length)], board_tile):
                return GameState.WON

        # Check diagonals
        diagonal_x = []
        diagonal_y = []
        for i in range(length):
            diagonal_x.append(self.board[i][i])
            diagonal_y.append(self.board[i][-(i + 1)])

        if check_list(diagonal_x, board_tile) or check_list(diagonal_y, board_tile):
            return GameState.WON

        # Check if draw
        for i in self.board:
            for j in i:
                if j == BoardTile.EMPTY:
                    return GameState.RUNNING

        return GameState.DRAW


def get_symbol(board_tile: BoardTile):
    if board_tile is None:
        return ""
    return MAPPINGS[board_tile.value]


def flatten_board(board, mark):
    lst = list(map(lambda tile: tile.value, [item for sublist in board for item in sublist]))
    lst.append(mark.value)
    return lst


def check_list(lst: list, board_tile: BoardTile):
    for i in lst:
        if i.value != board_tile.value:
            return False
    return True
