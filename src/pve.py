import os
import warnings

from src.Utils.Enums import GameState, BoardTile
from src.Actor.Bot import PretrainedBot
from src.Actor.Player import Player
from src.Game import GameEnv
from src.Utils import Exceptions

MODEL_PATH = "res/bot/1Mio_old"


def hide_warnings():
    def warn(*args, **kwargs):
        pass
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    warnings.warn = warn


def main():
    hide_warnings()

    player = Player(BoardTile.CROSS)
    bot = PretrainedBot(BoardTile.CIRCLE, 9, MODEL_PATH)
    game = GameEnv(player, bot)

    print("When entering a position, use: x, y")
    for i in range(9):
        stepper = game.get_stepper(i)
        is_bot = stepper == bot
        if is_bot:
            print("Bot is thinking...")

        while True:
            try:
                game.next_step(stepper)
                break
            except Exceptions.TileTakenException:
                if not is_bot:
                    print("This is place is already taken")
                    continue
                # Bot won't change the result unless the board gets modified.
                # This is an infinite it loops prevention, but shouldn't happen with a properly trained bot
                print("Bot made a invalid input")
                break

        if is_bot:
            print(game.receive_formatted_board())

        state = game.check_game_state(stepper.board_tile).value
        if state == GameState.WON.value:
            print(f"{stepper.board_tile.name} has won the game")
            break
        elif state == GameState.DRAW.value:
            print("Draw. Nobody won the game")
            break


if __name__ == "__main__":
    main()
