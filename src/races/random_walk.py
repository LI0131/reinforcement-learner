import random
import itertools

from typing import List, Tuple

from src.races.abstract import AbstractRace, HARSH


class RandomWalk(AbstractRace):

    def run(self) -> None:
        # possible acceleration options
        accelerations: List[Tuple[int, int]] = list(itertools.permutations([-1, 0, 1], 2))

        # run the algorithm until we reach the finish line
        x_o, y_o = self.car.x, self.car.y
        while not self.track.reached_finish(x_o, y_o, self.car.x, self.car.y):

            # make a random movement
            x_o, y_o = self.car.x, self.car.y
            a_index: int = random.randint(0, len(accelerations) - 1)
            self.car.set_acceleration(*accelerations[a_index])

            # apply any updates based on consequences
            if not self.track.is_valid(x_o, y_o, self.car.x, self.car.y):
                if HARSH:
                    self.car.x, self.car.y = self.track.starting_point
                    self.car.zeroize()
                else:
                    self.car.x, self.car.y = self.track.nearest_valid(x_o, y_o, self.car.x, self.car.y)
                    self.car.zeroize()

            # record values to history
            self.history.append(self.car.to_tuple())
