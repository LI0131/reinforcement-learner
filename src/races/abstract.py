import os
import time

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

    def move(self, a_x: int, a_y: int, nondeterministic: bool = True):
        # perform the movement
        x_o, y_o, v_xo, v_yo = self.car.to_tuple()
        self.car.set_acceleration(a_x, a_y, nondeterministic=nondeterministic)
        x_i, y_i, _, _ = self.car.to_tuple()
        self.history.append(((x_o, y_o, v_xo, v_yo), (a_x, a_y), self.car.to_tuple()))

        # validate the movement
        if not self.track.is_valid(x_o, y_o, x_i, y_i):
            if HARSH:
                self.car.x, self.car.y = self.track.starting_point
                self.car.zeroize()
            else:
                self.car.x, self.car.y = self.track.nearest_valid(x_o, y_o, x_i, y_i)
                self.car.zeroize()

            x_i, y_i, _, _ = self.car.to_tuple()

        # return whether or not the car has reached the finish line
        return self.track.reached_finish(x_o, y_o, x_i, y_i)

    def print_steps(self) -> None:
        for i, (x, y, _, _) in enumerate(self.history):
            self.track.print_track(x, y)
            time.sleep(0.5)
            if i < len(self.history) - 1:
                os.system('clear')
