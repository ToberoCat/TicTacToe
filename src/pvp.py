from src.Actor.Player import Player, GuiPlayer
from src.Utils.Enums import GameState, BoardTile
from src.Game import GameEnv
from src.Utils.Exceptions import TileTakenException
from src.Window import TicTacToeWindow


class Pvp:
    def __init__(self):
        self.game = GameEnv(Player(BoardTile.CROSS), Player(BoardTile.CIRCLE))
        self.window = TicTacToeWindow(self.execute, self.click)
        self.player = BoardTile.CROSS
        self.wins = {
            BoardTile.CROSS.value: 0,
            BoardTile.CIRCLE.value: 0
        }

        self.window.create_window()

    def execute(self):
        pass

    def click(self, x, y):
        try:
            self.game.next_step(GuiPlayer(self.player, x, y))
        except TileTakenException:
            return

        state = self.game.check_game_state(self.player)

        if state.value == GameState.WON.value:
            self.game = GameEnv(Player(BoardTile.CROSS), Player(BoardTile.CIRCLE))
            self.wins[self.player.value] += 1
        elif state.value == GameState.DRAW.value:
            self.game = GameEnv(Player(BoardTile.CROSS), Player(BoardTile.CIRCLE))

        if self.player.value == BoardTile.CROSS.value:
            self.player = BoardTile.CIRCLE
        else:
            self.player = BoardTile.CROSS

        self.window.update_window(self.game.board,
                                  self.wins[BoardTile.CROSS.value],
                                  self.wins[BoardTile.CIRCLE.value],
                                  self.player)


def main():
    Pvp()


if __name__ == "__main__":
    main()
