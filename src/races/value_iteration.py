import os
import time
import copy
import random
import itertools

import numpy as np

from src.races.abstract import AbstractRace

GAMMA: float = float(os.environ.get('GAMMA', 0.95))
LEARNING_RATE: float = float(os.environ.get('LEARNING_RATE', 0.1))
TRAINING_ITERS: int = int(os.environ.get('TRAINING_ITERS', 30))
THETA: float = float(os.environ.get('THETA', 0.1))


class ValueIteration(AbstractRace):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the default values for the algo
        self.actions = list(itertools.permutations([-1, 0, 1], 2))
        self.states: dict = {}
        self.Q: dict = {}
        self.policy: dict = {}

        # iterate over the potential states
        for x in range(self.track._x_max):
            for y in range(self.track._y_max):
                for v_x in range(-5, 6):
                    for v_y in range(-5, 6):
                        # define the initial state values
                        self.states[(x, y, v_x, v_y)] = random.random()
                        # define the initial Q values
                        if (x, y) in self.track._finishing_points:
                            self.Q[(x, y, v_x, v_y)] = [0 for _ in self.actions]
                        else:
                            self.Q[(x, y, v_x, v_y)] = [random.random() for _ in self.actions]

    def run(self) -> None:
        # create a boolean variable for convergence
        num_iters, max_q_delta = 0, float('inf')

        # loop until convergence is achieved
        while max_q_delta > THETA and num_iters < TRAINING_ITERS:

            # create a copy of the previous q-values table
            states_cpy = copy.deepcopy(self.states)

            # define the initial q-delta value to be zero
            max_q_delta: float = float('-inf')

            # iterate over the possible states
            for x in range(self.track._x_max):
                for y in range(self.track._y_max):
                    for v_x in range(-5, 6):
                        for v_y in range(-5, 6):

                            # skip invalid locations
                            if self.track._track[x][y] is False:
                                self.Q[(x, y, v_x, v_y)] = float('-inf')
                                continue

                            # define a variable to get the q-value of the best action
                            max_q: float = float('-inf')

                            # place holder for best policy action
                            best_policy = (0, 0)

                            # iterate over the set of possible actions and assign
                            # an updated value for each options
                            for j in range(len(self.actions)):

                                # set the new x, y, v_x, and v_y
                                self.car.x, self.car.y = x, y
                                self.car.v_x, self.car.v_y = v_x, v_y

                                # run the current action
                                finished = self.move(*self.actions[j], nondeterministic=False)

                                # compute the error based on successful movement and failed movement
                                exp: float = 0.8 * self.states[self.car.to_tuple()] + 0.2 * states_cpy[(x, y, v_x, v_y)]  # noqa

                                # get the reward and state values
                                reward: int = 0 if finished else -1

                                # update the Q values
                                new_q_value: float = reward + (GAMMA * exp)
                                self.Q[(x, y, v_x, v_y)][j] = new_q_value

                                # check if new_q is greater than max_q
                                if new_q_value > max_q:
                                    max_q = new_q_value
                                    best_policy = self.actions[j]

                            # reassign the values using the best action value max_q
                            old_q = self.states[(x, y, v_x, v_y)]
                            self.states[(x, y, v_x, v_y)] = max_q
                            self.policy[(x, y, v_x, v_y)] = best_policy

                            # check if the q_delta has been exceeded
                            q_delta: float = old_q - max_q
                            if q_delta > max_q_delta:
                                max_q_delta = q_delta

            num_iters += 1

        # set the car to the starting point
        self.history = []
        self.car.x, self.car.y = self.track.starting_point

        while True:
            # apply the policy to the car
            action = self.policy[self.car.to_tuple()]
            finished = self.move(*action)
            self.track.print_track(self.car.x, self.car.y)
            time.sleep(0.5)
            os.system('clear')

            # check to see if the car has reached the finish
            if finished:
                break
