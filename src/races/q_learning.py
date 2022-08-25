import os
import time
import random

import numpy as np

from typing import List

from src.races.abstract import AbstractRace

GAMMA: float = float(os.environ.get('GAMMA', 0.95))
EPSILON: float = float(os.environ.get('EPSILON', 0.5))
LEARNING_RATE: float = float(os.environ.get('LEARNING_RATE', 0.99))
DECAY: float = float(os.environ.get('DECAY', 0.001))
MAX_STEPS: int = int(os.environ.get('MAX_STEPS', 10000))
TRAINING_ITERS: int = int(os.environ.get('TRAINING_ITERS', 5000))
reward: int = -1


class QLearning(AbstractRace):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # define Q table
        self.Q = {}
        for x in range(self.track._x_max):
            for y in range(self.track._y_max):
                for v_x in range(-5, 6):
                    for v_y in range(-5, 6):
                        self.Q[(x, y, v_x, v_y)] = -1 * np.random.rand(3, 3)

        # collect loss results
        self.loss_values: List[int] = []

    def best_action(self, q_value):
        return np.unravel_index(q_value.argmax(), q_value.shape)

    def choose_action(self, q_value, epsilon):
        if random.random() < epsilon:
            ai_x, ai_y = (np.random.randint(3), np.random.randint(3))
        else:
            ai_x, ai_y = self.best_action(q_value)

        return ai_x, ai_y

    def run(self) -> None:
        # create local version of epsilon to update with decay over time
        epsilon = EPSILON

        # Train through the specified number of training iterations
        for i in range(TRAINING_ITERS):
            os.system('clear')
            print(f'Training Completed: {round(i / TRAINING_ITERS, 3) * 100}%')

            # set the location and velocity of the car
            self.car.x, self.car.y = self.track.starting_point
            self.car.zeroize()

            # train the car to find the finish
            finished, num_steps = False, 0
            while not finished and num_steps < MAX_STEPS:

                # get the next action
                x, y, v_x, v_y = self.car.to_tuple()
                selected_q = self.Q[(x, y, v_x, v_y)]
                ai_x, ai_y = self.choose_action(selected_q, epsilon)
                q_o = selected_q[ai_x][ai_y]
                action = [ai_x - 1, ai_y - 1]

                # update the car's position
                finished = self.move(*action)

                # get the next state
                q_i = self.Q[self.car.to_tuple()]

                # Update the Q table for the current state-action pair
                action_space: np.array = self.Q[(x, y, v_x, v_y)]
                action_space[ai_x, ai_y] += LEARNING_RATE * (reward + (GAMMA * q_i.max()) - q_o)
                self.Q[(x, y, v_x, v_y)] = action_space

                # increment step count
                num_steps += 1

            # Gradually reduce epsilon through the process
            epsilon -= DECAY

            # add loss for iteration to memory
            self.loss_values.append(self.loss)
            self.history = []

        print('Racing...')
        self.car.x, self.car.y = self.track.starting_point
        self.car.zeroize()
        time.sleep(1)

        while True:
            # apply the policy to the car
            x_o, y_o, v_x, v_y = self.car.to_tuple()
            qval = self.Q[(x_o, y_o, v_x, v_y)]
            # print(qval)
            ai_x, ai_y = self.choose_action(qval, 0.1)
            # print(ai_x - 1, ai_y - 1)
            finished = self.move(ai_x - 1, ai_y - 1)
            self.track.print_track(self.car.x, self.car.y)
            os.system('clear')

            # check to see if the car has reached the finish
            if finished:
                break
