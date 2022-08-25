from __future__ import annotations

import copy
import math
import random

from typing import Tuple, List


class Track:
    
    def __init__(
        self,
        x_max: int,
        y_max: int,
        grid: List[List[bool]],
        start: List[Tuple[int, int]],
        finish: List[Tuple[int, int]]
    ):
        self._x_max: int = x_max
        self._y_max: int = y_max
        self._track: List[List[bool]] = grid
        self._starting_points: List[Tuple[int, int]] = start
        self._finishing_points: List[Tuple[int, int]] = finish

    @property
    def starting_point(self) -> Tuple[int, int]:
        return self._starting_points[random.randint(0, len(self._starting_points) - 1)]

    @classmethod
    def from_file(cls, filepath: str) -> Track:
        # define the default variable values
        track: List[List[bool]] = []
        start: List[Tuple[int, int]] = []
        finish: List[Tuple[int, int]] = []

        # read track from the file
        with open(filepath) as racetrack:
            lines = [l.strip() for l in racetrack.readlines()]

            # read the size of the track
            x_max, y_max = lines[0].split(',')

            # read the track info
            for i in range(1, len(lines)):
                row: List[bool] = []
                for j in range(len(lines[i])):
                    if lines[i][j] == '#':
                        row.append(False)
                    elif lines[i][j] == '.':
                        row.append(True)
                    elif lines[i][j] == 'S':
                        row.append(True)
                        start.append((i - 1, j))
                    elif lines[i][j] == 'F':
                        row.append(True)
                        finish.append((i - 1, j))
                    else:
                        raise ValueError(f'Unrecognized symbol: {lines[i][j]}')
                track.append(row)

        return cls(int(x_max), int(y_max), track, start, finish)

    def print_track(self, x: int, y: int) -> None:
        output: str = ''
        track_cpy = copy.deepcopy(self._track)
        track_cpy[x][y] = 'X'
        for row in track_cpy:
            rowstr: str = ''
            for item in row:
                if item == 'X':
                    rowstr += item
                elif item:
                    rowstr += '.'
                else:
                    rowstr += '#'

            output += rowstr + '\n'

        print(output, end='\r', flush=True)

    def _bresenham(self, x_o, y_o, x, y) -> List[Tuple[int, int]]:
        '''
        Return the set of all points that occur between (x_o, y_o) and (x, y)
        when connected by a straight line.

        :param x_o: the initial x
        :param y_o: the initial y
        :param x: the desired x
        :param y: the desired y
        :return: the list of effected points
        '''
        # compute the change in both values
        delta_x = x - x_o
        delta_y = y - y_o

        xp: int = 1 if delta_x > 0 else -1
        yp: int = 1 if delta_y > 0 else -1

        dx_p, dy_p = abs(delta_x), abs(delta_y)

        # get the initial values for each parameter
        if dx_p > dy_p:
            x_y, y_x = 0, 0
        else:
            dx_p, dy_p = dy_p, dx_p
            xp, x_y, y_x, yp = 0, yp, xp, 0

        # create the y iterator and the accumulator delta
        delta = 2 * dy_p - dx_p
        y_i = 0

        # get the intersected points
        intersected: List[Tuple[int, int]] = []
        for x_i in range(dx_p + 1):
            intersected.append((x_o + x_i * xp + y_i * y_x, y_o + x_i * x_y + y_i * yp))
            if delta >= 0:
                y_i += 1
                delta -= 2 * dx_p
            delta += 2 * dy_p

        # return the intersected points
        return intersected

    def is_valid(self, x_o: int, y_o: int, x: int, y: int) -> bool:
        '''
        Check whether or not the next chosen point is a valid selection (i.e. it
        does not collide with a wall inbetween)

        :param x_o: the initial x
        :param y_o: the initial y
        :param x: the desired x
        :param y: the desired y
        :return: a boolean for path validity
        '''
        if x < self._x_max and x >= 0 and y < self._y_max and y >= 0:
            intersected_points = self._bresenham(x_o, y_o, x, y)
            for (x_i, y_i) in intersected_points:
                if not self._track[x_i][y_i]:
                    return False
            return True
        else:
            return False

    def nearest_valid(self, x_o: int, y_o: int, x: int, y: int) -> Tuple[int, int]:
        '''
        Find the closest valid point to the desired movement location.

        :param x_o: the initial x
        :param y_o: the initial y
        :param x: the desired x
        :param y: the desired y
        :return: the closest valid point to move to
        '''
        if self.is_valid(x_o, y_o, x, y):
            return x, y
        else:
            min_distance, loc = float('inf'), None
            for i in range(self._x_max):
                for j in range(self._y_max):
                    if self.is_valid(x_o, y_o, i, j):
                        distance: float = math.dist((x, y), (i, j))
                        if distance < min_distance:
                            min_distance, loc = distance, (i, j)
                    else:
                        continue

            return loc

    def reached_finish(self, x_o: int, y_o: int, x: int, y: int) -> bool:
        '''
        Determine whether or not the car has crossed the finish line

        :param x_o: the initial x
        :param y_o: the initial y
        :param x: the desired x
        :param y: the desired y
        :return: whether or not the car crossed the finish line
        '''
        traversed_coords = self._bresenham(x_o, y_o, x, y)
        for coord in traversed_coords:
            if coord in self._finishing_points:
                return True
        return False


if __name__ == '__main__':
    track = Track.from_file('/Users/liammccann/Documents/git_repositories/reinforcement-learner/tracks/R-track.txt')
    track = Track.from_file('/Users/liammccann/Documents/git_repositories/reinforcement-learner/tracks/O-track.txt')
    track = Track.from_file('/Users/liammccann/Documents/git_repositories/reinforcement-learner/tracks/L-track.txt')
