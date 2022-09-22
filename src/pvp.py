from src.Actor.Player import Player
from src.Utils.Enums import GameState, BoardTile
from src.Game import GameEnv
from src.Utils import Exceptions


def main():
    game = GameEnv(Player(BoardTile.CROSS), Player(BoardTile.CIRCLE))

    print("When entering a position, use: x, y")
    for i in range(9):
        stepper = game.get_stepper(i)

        while True:
            try:
                game.next_step(stepper)
                break
            except Exceptions.TileTakenException:
                print("This is place is already taken")
                continue

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
