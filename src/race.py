import os
import random

from typing import List, Tuple

from src.car import Car
from src.track import Track

HARSH: bool = os.environ.get('HARSH', 'false').lower() == 'true'


class AbstractRace:

    def __init__(self, trackfile: str):
        self.track = Track.from_file(trackfile)
        self.car = Car(*self.track.starting_point)
        self.history: List[Tuple] = []

    @property
    def loss(self) -> int:
        return len(self.history)

    def run(self) -> None:
        raise NotImplementedError


class RandomWalk(AbstractRace):

    def run(self) -> None:
        # run the algorithm until we reach the finish line
        while not self.track.reached_finish(self.car.x, self.car.y):

            # make a random movement
            r: float = random.random()
            if r >= 0 and r < 0.25:
                self.car.accelerate_x()
            elif r >= 0.25 and r < 0.5:
                self.car.accelerate_y()
            elif r >= 0.5 and r < 0.75:
                self.car.decelerate_x()
            else:
                self.car.decelerate_y()

            # record values to history
            print(self.car.to_tuple())
            self.history.append(self.car.to_tuple())

            # evaluate consequences
            is_valid: bool = self.track.is_valid(self.car.x, self.car.y)

            # apply any updates based on consequences
            if not is_valid:
                if HARSH:
                    self.car.x, self.car.y = self.track.starting_point
                    self.car.zeroize()
                else:
                    self.car.x, self.car.y = self.track.nearest_valid(self.car.x, self.car.y)
                    self.car.zeroize()
