import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import adam_v2

from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy
from tensorflow import keras

from src.Actor.BaseActor import BaseActor
from src.Utils.Enums import BoardTile
from src.Game import flatten_board


class Bot(BaseActor):
    def __init__(self, board_tile: BoardTile, model, actions):
        super().__init__(board_tile)
        self.model = model
        self.dqn = self.build_agent(actions)

    def build_agent(self, actions):
        policy = BoltzmannQPolicy()
        memory = SequentialMemory(limit=50000, window_length=1)
        dqn = DQNAgent(model=self.model, memory=memory, policy=policy, nb_actions=actions,
                       nb_steps_warmup=50, target_model_update=1e-2)
        dqn.compile(optimizer=adam_v2.Adam(learning_rate=1e-3), metrics=['mae'])
        return dqn

    def request(self) -> tuple:
        flat = np.array(flatten_board(self.board, self.board_tile)).reshape((-1, 10))

        seq = self.model.predict(np.array([flat, ]))[0]
        action = np.argmax(seq)
        x = action // 3
        y = action % 3

        return x, y


def build_model(states, actions):
    model = Sequential()
    model.add(Dense(48, activation='relu', input_shape=(1, int(states + 1))))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(12, activation='relu'))
    model.add(Dense(9, activation='relu'))
    model.add(Flatten())
    model.add(Dense(actions, activation='linear'))

    return model


class TrainingBot(Bot):
    def __init__(self, board_tile: BoardTile, states, actions):
        super().__init__(board_tile, build_model(states, actions), actions)


class PretrainedBot(Bot):
    def __init__(self, board_tile: BoardTile, actions, last_model):
        super().__init__(board_tile, keras.models.load_model(last_model), actions)
