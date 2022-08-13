from __future__ import annotations

import math

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
        return self._starting_points[0]

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
                        start.append((i, j))
                    elif lines[i][j] == 'F':
                        row.append(True)
                        finish.append((i, j))
                    else:
                        raise ValueError(f'Unrecognized symbol: {lines[i][j]}')
                track.append(row)

        return cls(int(x_max), int(y_max), track, start, finish)

    def is_valid(self, x: int, y: int) -> bool:
        if x < self._x_max and x >= 0 and y < self._y_max and y >= 0:
            return self._track[x][y]
        else:
            return False

    def nearest_valid(self, x: int, y: int) -> Tuple[int, int]:
        if self.is_valid(x, y):
            return x, y
        else:
            min_distance, loc = float('inf'), None
            for i in range(self._x_max):
                for j in range(self._y_max):
                    if self.is_valid(i, j):
                        distance: float = math.sqrt((x + i) ** 2 + (y + j) ** 2)
                        if distance < min_distance:
                            min_distance, loc = min_distance, (i, j)
                    else:
                        continue
            return loc

    def reached_finish(self, x: int, y: int) -> bool:
        return (x, y) in self._finishing_points


if __name__ == '__main__':
    track = Track.from_file('/Users/liammccann/Documents/git_repositories/reinforcement-learner/tracks/R-track.txt')
    track = Track.from_file('/Users/liammccann/Documents/git_repositories/reinforcement-learner/tracks/O-track.txt')
    track = Track.from_file('/Users/liammccann/Documents/git_repositories/reinforcement-learner/tracks/L-track.txt')
