import os
from typing import Optional

from wandb.keras import WandbCallback
import wandb

import numpy as np
from gym import Env
from gym.spaces import Discrete, Box
from rl.callbacks import FileLogger, ModelIntervalCheckpoint

from src.Callbacks import BestModelCallback
from src.Game import GameEnv, flatten_board
from src.Actor.Bot import TrainingBot, PretrainedBot, Bot
from src.Actor.BaseActor import BaseActor
from src.Utils.Enums import BoardTile, GameState
from src.Utils import Exceptions

NO_REWARD = 0
WON_REWARD = 1
LOSE_REWARD = -1
DRAW_REWARD = 0.0001
INVALID_INPUT_REWARD = -5
EPISODES = 1e6
MODEL_PATH = "res/bot/1Mio_old"


class TrainEnv(Env):

    def __init__(self):
        self.action_space = Discrete(9)
        self.observation_space = Box(low=np.array([0]), high=np.array([2]))

        self.game = GameEnv(None, None)
        self.counter = 0

    def step(self, action: int):
        info = {"wins": 0, "draws": 0}
        x = action // 3
        y = action % 3

        # Make first action
        current_tile = BoardTile.CROSS if self.counter % 2 == 0 else BoardTile.CIRCLE
        opposite_tile = BoardTile.CROSS if self.counter % 2 == 1 else BoardTile.CIRCLE

        self.counter += 1
        reward = NO_REWARD
        try:
            self.game.next_step(ActionStepper(current_tile, x, y))
        except Exceptions.TileTakenException:
            reward += INVALID_INPUT_REWARD

        # Check if the game is won
        done = False
        state = self.game.check_game_state(current_tile).value
        if state == GameState.WON.value:
            reward += WON_REWARD
            info["wins"] = 1
            done = True
        elif state == GameState.DRAW.value:
            done = True
            info["draws"] = 1
            reward += DRAW_REWARD

        state = self.game.check_game_state(opposite_tile).value
        if state == GameState.WON.value:
            reward -= LOSE_REWARD
            info["wins"] = 1
            done = True

        if self.counter >= 9:
            done = True
            info["draws"] = 1
            reward += DRAW_REWARD

        info["placed-items"] = self.counter

        if done:
            wandb.log(info)
        return flatten_board(self.game.board, current_tile), reward, done, info

    def reset(
            self,
            *,
            seed: Optional[int] = None,
            options: Optional[dict] = None,
    ):
        self.game.reset_board()
        self.counter = 0
        return flatten_board(self.game.board, BoardTile.CROSS)

    def render(self, mode):
        print(self.game.receive_formatted_board())


class ActionStepper(BaseActor):

    def __init__(self, board_tile: BoardTile, x, y):
        super().__init__(board_tile)
        self.x = x
        self.y = y

    def request(self) -> tuple:
        return self.x, self.y


def test_env():
    episodes = 10
    env = TrainEnv()
    for episode in range(1, episodes + 1):
        state = env.reset()
        print(state)
        done = False
        score = 0

        while not done:
            # env.render()
            action = env.action_space.sample()
            n_state, reward, done, info = env.step(action)
            score += reward

        print(f"Episode: {episode} finished with a score of {score}")


class BotTrainer:

    def __init__(self, model_path, episodes):
        self.model_path = model_path
        self.episodes = episodes

    def train_from_start(self):
        bot = TrainingBot(BoardTile.CROSS, 9, 9)
        self.__train(bot)

    def continue_training(self):
        bot = PretrainedBot(BoardTile.CROSS, 9, self.model_path, True)

        items = sorted(list(map(lambda x: int(x), os.listdir(self.model_path + "/checkpoints"))))

        self.episodes -= items[-1]
        self.__train(bot)

    def __train(self, bot: Bot):
        env = TrainEnv()
        bot.model.summary()

        if not os.path.exists(self.model_path + "/last"):
            os.makedirs(self.model_path + "/last")

        wandb.config = {
            "episodes": self.episodes
        }

        callbacks = [
            BestModelCallback(self.model_path + "/best"),
            ModelIntervalCheckpoint(self.model_path + "/checkpoints/{step}/weights.h5f", interval=10000),
            FileLogger(self.model_path + "/last/dqn_log.json", interval=100),
            WandbCallback()
        ]
        try:
            bot.dqn.fit(env, callbacks=callbacks, nb_steps=self.episodes, visualize=False, verbose=1)
        except BaseException:
            print("Error while training")

        bot.model.save(self.model_path + "/last", overwrite=True)

        bot.dqn.test(env, nb_episodes=1, visualize=True)


def main():
    wandb.init(project="train", entity="tobero")

    bot_trainer = BotTrainer(MODEL_PATH, EPISODES)
    bot_trainer.train_from_start()


def continue_training():
    wandb.init(project="train", entity="tobero", resume=True)
    bot_trainer = BotTrainer(MODEL_PATH, EPISODES)
    bot_trainer.continue_training()


if __name__ == "__main__":
    # main()
    continue_training()
