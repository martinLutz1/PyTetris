from copy import deepcopy
import pygame
from typing import Optional
import numpy
import random
import time
from Figures import *


class Tetris:
    number_of_rows: int
    number_of_columns: int
    field: numpy.ndarray
    moving_figure: Figure
    ms_elapsed_since_last_step: int
    ms_elapsed_since_last_move: int
    update_interval_ms: int
    min_move_interval_ms: int

    def __init__(self, number_of_rows: int, number_of_columns: int):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.field = numpy.full(
            (number_of_rows, number_of_columns), Optional[pygame.Color])
        self.ms_elapsed_since_last_step = 0
        self.ms_elapsed_since_last_move = 0
        self.update_interval_ms = 500
        self.min_move_interval_ms = 50

        self.spawn_figure(Position(number_of_columns / 2, 1))

    def spawn_figure(self, position: Position):
        figure_type = random.choice(list(FigureBuilder.FigureType))
        self.moving_figure = (FigureBuilder.new(position, figure_type))

    def _move_collides(self, figure: Figure, direction: Direction) -> bool:
        for used_point in figure.get_next_move_used_points(direction):
            # Horizontal border collision
            if (used_point.x < 0) or (used_point.x >= self.number_of_columns):
                return True
            # Vertical border collision
            if (used_point.y < 0) or (used_point.y >= self.number_of_rows):
                return True
            # Field contains already a block
            if self.field[int(
                    used_point.y)][int(used_point.x)] != None:
                return True

        return False

    # Returns whether a new figure is spawned or not
    def _move_internal(self, direction: Direction) -> bool:
        if not self._move_collides(self.moving_figure, direction):
            self.moving_figure.move(direction)
            return False

        if direction == Direction.DOWN:
            for used_point in self.moving_figure.get_used_points():
                self.field[int(used_point.y)][int(used_point.x)
                                              ] = self.moving_figure.color

            self.spawn_figure(Position(self.number_of_columns / 2, 1))
            # New spawned figure collides on spawn -> gameover
            if self._move_collides(self.moving_figure, direction):
                # TODO: Handle gameover
                self.field = numpy.full(
                    (self.number_of_rows, self.number_of_columns), None)
                self.spawn_figure(Position(self.number_of_columns / 2, 1))
            return True
        return False

    # Returns whether a new figure is spawned or not
    def move(self, direction: Direction) -> bool:
        # Avoid too fast interaction
        ms_elapsed_now = time.time() * 1000
        if (ms_elapsed_now - self.ms_elapsed_since_last_move) < self.min_move_interval_ms:
            return False

        is_new_figure_spawned = self._move_internal(direction)
        self.ms_elapsed_since_last_move = ms_elapsed_now
        return is_new_figure_spawned

    # Returns true if row is scored.
    def check_rows(self) -> bool:
        rows_to_delete = []
        for y in range(self.number_of_rows):
            if not (None in self.field[y]):
                rows_to_delete.append(y)

        self.field = numpy.delete(self.field, rows_to_delete, axis=0)
        self.field = numpy.insert(self.field, numpy.zeros(
            len(rows_to_delete), dtype=int), None, axis=0)

        return len(rows_to_delete) > 0

    # Returns whether a new figure is spawned or not
    def update(self) -> bool:
        is_new_figure_spawned = False

        ms_elapsed_now = time.time() * 1000
        if (ms_elapsed_now - self.ms_elapsed_since_last_step) > self.update_interval_ms:
            is_new_figure_spawned = self._move_internal(Direction.DOWN)
            self.ms_elapsed_since_last_step = ms_elapsed_now
        return is_new_figure_spawned
