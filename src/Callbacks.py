import os
import timeit

import numpy as np
import wandb
from rl.callbacks import Callback


class BestModelCallback(Callback):
    def __init__(self, logdir: str):
        super().__init__()
        self.lastloss = 200
        self.lastepisode = 0
        self.logdir = logdir
        self.metrics = {}
        self.starts = {}
        self.data = {}
        self.runs = 0

    def _set_env(self, env):
        self.env = env

    def on_train_begin(self, logs=None):
        """ Initialize model metrics before training """
        self.metrics_names = self.model.metrics_names

    def on_episode_begin(self, episode, logs=None):
        """ Initialize metrics at the beginning of each episode """
        assert episode not in self.metrics
        assert episode not in self.starts
        self.metrics[episode] = []
        self.starts[episode] = timeit.default_timer()

    def on_episode_end(self, episode, logs=None):
        """ Compute and print metrics at the end of each episode """
        metrics = self.metrics[episode]
        if np.isnan(metrics).all():
            mean_metrics = np.array([np.nan for _ in self.metrics_names])
        else:
            mean_metrics = np.nanmean(metrics, axis=0)
        assert len(mean_metrics) == len(self.metrics_names)

        data = dict(zip(self.metrics_names, mean_metrics))
        data.update(logs)
        wandb.log(data)

        if self.runs > 1000:
            if self.lastloss > data["loss"]:
                self.lastloss = data["loss"]
                self.lastepisode = episode
                new_weights = f'{self.logdir}/best_weights.h5f'
                self.model.save_weights(new_weights, overwrite=True)

        # Clean up.
        del self.metrics[episode]
        del self.starts[episode]

    def on_step_end(self, step, logs=None):
        """ Append metric at the end of each step """
        self.metrics[logs['episode']].append(logs['metrics'])
        self.runs += 1
