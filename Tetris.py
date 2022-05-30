from copy import deepcopy
from typing import Optional
import numpy
import random
import time
from Figures import *
from Player import Player


class StatusInfo:
    ms_elapsed_since_last_step: int = 0
    ms_elapsed_since_last_move: int = 0
    has_moved: bool = False
    has_spawned_figure: bool = False
    is_game_over: bool = False


class Tetris:
    start_update_interval_ms: int = 500
    min_update_interval_ms: int = 250
    min_move_interval_ms: int = 50

    number_of_rows: int
    number_of_columns: int
    update_interval_ms: int
    field: numpy.ndarray
    moving_figure: Figure
    status_info = StatusInfo()
    player = Player()

    def __init__(self, number_of_rows: int, number_of_columns: int):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self._start_new_game()

    def spawn_figure(self, position: Position):
        figure_type = random.choice(list(FigureBuilder.FigureType))
        self.moving_figure = (FigureBuilder.new(position, figure_type))
        self.status_info.has_spawned_figure = True

    def _move_collides(self, figure: Figure, direction: Direction) -> bool:
        for block in figure.get_blocks_for_next_move(direction):
            # Horizontal border collision
            if (block.x < 0) or (block.x >= self.number_of_columns):
                return True
            # Vertical border collision
            if (block.y < 0) or (block.y >= self.number_of_rows):
                return True
            # Field contains already a block
            if self.field[block.y][block.x] is not None:
                return True

        return False

    def _start_new_game(self):
        self.field = numpy.full(
            (self.number_of_rows, self.number_of_columns), None)
        self.spawn_figure(Position(int(self.number_of_columns / 2), 1))
        self.status_info.is_game_over = True
        self.update_interval_ms = self.start_update_interval_ms
        self.player.reset()

    def _move_internal(self, direction: Direction):
        if not self._move_collides(self.moving_figure, direction):
            self.moving_figure.move(direction)
            self.status_info.has_moved = True
            return

        if direction == Direction.DOWN:
            for block in self.moving_figure.get_blocks():
                self.field[block.y][block.x] = self.moving_figure.block_color

            self.spawn_figure(Position(int(self.number_of_columns / 2), 1))

            # New spawned figure collides on spawn -> gameover
            if self._move_collides(self.moving_figure, direction):
                self._start_new_game()

            self.status_info.has_moved = True

    def move(self, direction: Direction):
        # Avoid too fast interaction
        ms_elapsed_now = time.time() * 1000
        if (ms_elapsed_now - self.status_info.ms_elapsed_since_last_move) < self.min_move_interval_ms:
            return

        self._move_internal(direction)
        self.status_info.ms_elapsed_since_last_move = ms_elapsed_now

    # Returns true if row is scored.
    def check_rows(self) -> bool:
        rows_to_delete = []
        for y in range(self.number_of_rows):
            if not (None in self.field[y]):
                rows_to_delete.append(y)

        if len(rows_to_delete) == 0:
            return False

        self.field = numpy.delete(self.field, rows_to_delete, axis=0)
        self.field = numpy.insert(self.field, numpy.zeros(
            len(rows_to_delete), dtype=int), None, axis=0)

        scoring_points = 100 * len(rows_to_delete) * len(rows_to_delete)
        self.player.add_to_score(scoring_points)

        def update_game_speed():
            self.update_interval_ms = self.start_update_interval_ms - \
                int(self.player.score / 20)
            self.update_interval_ms = max(
                self.min_update_interval_ms, self.update_interval_ms)
            self.update_interval_ms = min(
                self.start_update_interval_ms, self.update_interval_ms)
        update_game_speed()
        return True

    def update(self):
        ms_elapsed_now = time.time() * 1000
        if (ms_elapsed_now - self.status_info.ms_elapsed_since_last_step) > self.update_interval_ms:
            self._move_internal(Direction.DOWN)
            self.status_info.ms_elapsed_since_last_step = ms_elapsed_now

    def has_spawned_figure(self):
        has_spawned_figure = self.status_info.has_spawned_figure
        self.status_info.has_spawned_figure = False
        return has_spawned_figure

    def has_moved(self):
        has_moved = self.status_info.has_moved
        self.status_info.has_moved = False
        return has_moved

    def is_game_over(self):
        is_game_over = self.status_info.is_game_over
        self.status_info.is_game_over = False
        return is_game_over
