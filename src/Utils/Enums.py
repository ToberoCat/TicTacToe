from enum import Enum


class GameState(Enum):
    WON = 0
    DRAW = 1
    RUNNING = 2


class BoardTile(Enum):
    EMPTY = 0
    CROSS = 1
    CIRCLE = 2
