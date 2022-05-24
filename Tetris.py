import numpy
import random
import time
from Figures import *


class Tetris:
    number_of_rows: int
    number_of_columns: int
    field: numpy.ndarray
    figures: list[Figure]
    ms_elapsed_since_last_step: int
    ms_elapsed_since_last_move: int
    update_interval_ms: int
    min_move_interval_ms: int

    def __init__(self, number_of_rows: int, number_of_columns: int):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.field = numpy.full((number_of_columns, number_of_rows), False)
        self.figures = []
        self.ms_elapsed_since_last_step = 0
        self.ms_elapsed_since_last_move = 0
        self.update_interval_ms = 500
        self.min_move_interval_ms = 50

        self.spawn_figure(Position(number_of_columns / 2, 1))

    def spawn_figure(self, position: Position):
        figure_type = random.choice(list(FigureBuilder.FigureType))
        self.figures.append(FigureBuilder.new(position, figure_type))

    def _move_collides(self, figure: Figure, direction: Direction) -> bool:

        def collides(position: Position, direction: Direction):
            match direction:
                case Direction.UP:
                    return False
                case Direction.RIGHT:
                    new_x_position = position.x + 1
                    if new_x_position >= self.number_of_columns:
                        return True
                    return self.field[int(
                        new_x_position)][int(position.y)]
                case Direction.LEFT:
                    new_x_position = position.x - 1
                    if new_x_position < 0:
                        return True
                    return self.field[int(new_x_position)][int(position.y)]
                case Direction.DOWN:
                    new_y_position = position.y + 1
                    if new_y_position >= self.number_of_rows:
                        return True
                    return self.field[int(
                        position.x)][int(new_y_position)]

        for used_point in figure.get_next_move_used_points(direction):
            # Horizontal border collision
            if (used_point.x < 0) or (used_point.x >= self.number_of_columns):
                return True
            # Vertical border collision
            if (used_point.y < 0) or (used_point.y >= self.number_of_rows):
                return True
            if self.field[int(
                    used_point.x)][int(used_point.y)]:
                return True

        return False

    def _move_internal(self, direction: Direction):
        if self._move_collides(self.figures[-1], direction):
            if direction == Direction.DOWN:
                for used_point in self.figures[-1].get_used_points():
                    self.field[int(used_point.x)][int(used_point.y)] = True
                self.spawn_figure(Position(self.number_of_columns / 2, 1))
                if self._move_collides(self.figures[-1], direction):
                    # TODO: Handle gameover
                    self.figures = []
                    self.field = numpy.full(
                        (self.number_of_columns, self.number_of_rows), False)
                    self.spawn_figure(Position(self.number_of_columns / 2, 1))
            return
        self.figures[-1].move(direction)

    def move(self, direction: Direction):
        # Avoid too fast interaction
        ms_elapsed_now = time.time() * 1000
        if (ms_elapsed_now - self.ms_elapsed_since_last_move) < self.min_move_interval_ms:
            return
        self._move_internal(direction)
        self.ms_elapsed_since_last_move = ms_elapsed_now

    def update(self):
        ms_elapsed_now = time.time() * 1000
        if (ms_elapsed_now - self.ms_elapsed_since_last_step) > self.update_interval_ms:
            self._move_internal(Direction.DOWN)
            self.ms_elapsed_since_last_step = ms_elapsed_now
