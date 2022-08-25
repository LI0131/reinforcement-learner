import random

from typing import Tuple


class Car:

    def __init__(self, x_initial: int, y_initial: int):
        self.x: int = x_initial
        self.y: int = y_initial
        self.v_x: int = 0
        self.v_y: int = 0

    def _can_change(self):
        return random.random() < 0.8

    def _update_x(self, a_x: int):
        # update the velocity if in acceptable range
        v_x = a_x + self.v_x
        if v_x > -5 and v_x < 5:
            self.v_x = v_x

        # update position based on speed
        self.x = self.v_x + self.x
    
    def _update_y(self, a_y: int):
        # update the velocity if in acceptable range
        v_y = a_y + self.v_y
        if v_y > -5 and v_y < 5:
            self.v_y = v_y

        # update position based on speed
        self.y = self.v_y + self.y

    def set_acceleration(self, a_x: int, a_y: int, nondeterministic: bool = True) -> None:
        if not nondeterministic or self._can_change():
            self._update_x(a_x)
            self._update_y(a_y)

    def zeroize(self):
        self.v_x, self.v_y = 0, 0

    def to_tuple(self) -> Tuple[int, int, int, int]:
        return (self.x, self.y, self.v_x, self.v_y)
