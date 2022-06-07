from copy import deepcopy
from turtle import left
import numpy
import random
from FigureBuilder import FigureBuilder
from Figures import *
from Player import Player


class StatusInfo:
    ms_elapsed_since_last_move: int = 0
    has_moved: bool = False
    has_spawned_figure: bool = False
    is_game_over: bool = False


class Tetris:
    start_update_interval_ms: int = 500
    min_update_interval_ms: int = 250
    manual_movement_duration_ms: int = 30

    number_of_rows: int
    number_of_columns: int
    update_interval_ms: int
    field: numpy.ndarray
    moving_figure: Figure = None
    last_figure: Figure = None
    status_info = StatusInfo()
    player = Player()

    def __init__(self, number_of_rows: int, number_of_columns: int):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self._start_new_game()

    def spawn_figure(self, position: BlockPosition):
        if self.moving_figure:
            self.last_figure = self.moving_figure

        figure_type = random.choice(list(FigureBuilder.FigureType))
        self.moving_figure = (FigureBuilder.new(position, figure_type))
        self.status_info.has_spawned_figure = True

    def _move_collides(self, figure: Figure, direction: Direction) -> bool:
        is_moving_down = figure.moves_down()
        is_moving_right = figure.moves_right()
        is_moving_left = figure.moves_left()

        def block_collides(block_position: BlockPosition):
            block_to_be_checked = [block_position]

            if is_moving_right:
                block_to_be_checked.append(BlockPosition(
                    block_position.x + 1, block_position.y))

            if is_moving_left:
                block_to_be_checked.append(BlockPosition(
                    block_position.x - 1, block_position.y))

            if is_moving_down:
                block_to_be_checked.append(BlockPosition(
                    block_position.x, block_position.y + 1))

            # Border collision
            if any(position.x >= self.number_of_columns for position in block_to_be_checked):
                return True
            if any(position.x < 0 for position in block_to_be_checked):
                return True
            if any(position.y >= self.number_of_rows for position in block_to_be_checked):
                return True

            # Block collision
            if any(self.field[position.y][position.x] for position in block_to_be_checked):
                return True

            if direction == Direction.down:
                if self.field[block_position.y - 1][block_position.x]:
                    return True

            return False

        for block_position in figure.get_blocks_for_next_move(direction):
            if block_collides(block_position):
                return True

        return False

    def _start_new_game(self):
        self.field = numpy.full(
            (self.number_of_rows, self.number_of_columns), None)
        self.spawn_figure(BlockPosition(int(self.number_of_columns / 2), 1))
        self.status_info.is_game_over = True
        self.update_interval_ms = self.start_update_interval_ms
        self.player.reset()

    def _move_internal(self, direction: Direction, duration_ms: int):
        if not self._move_collides(self.moving_figure, direction):
            self.moving_figure.move(direction, duration_ms)
            self.status_info.has_moved = True
            return

        # Collision on down movement -> Spawn a new figure
        if direction == Direction.down:
            self.moving_figure.finalize()
            for block in self.moving_figure.get_blocks():
                self.field[block.y][block.x] = self.moving_figure.block_color

            self.spawn_figure(BlockPosition(
                int(self.number_of_columns / 2), 1))

            # New spawned figure collides on spawn -> Gameover
            if self._move_collides(self.moving_figure, direction):
                self._start_new_game()

            self.moving_figure.move(direction.down, duration_ms)
            self.status_info.has_moved = True

    def move(self, direction: Direction):
        self._move_internal(direction, self.manual_movement_duration_ms)

    # Returns list of scored rows.
    def check_rows(self) -> List[int]:
        scored_rows = []
        for y in range(self.number_of_rows):
            if not (None in self.field[y]):
                scored_rows.append(y)

        if len(scored_rows) > 0:
            self.field = numpy.delete(self.field, scored_rows, axis=0)
            self.field = numpy.insert(self.field, numpy.zeros(
                len(scored_rows), dtype=int), None, axis=0)

            scoring_points = 100 * len(scored_rows) * len(scored_rows)
            self.player.add_to_score(scoring_points)

            def update_game_speed():
                self.update_interval_ms = self.start_update_interval_ms - \
                    int(self.player.score / 20)
                self.update_interval_ms = max(
                    self.min_update_interval_ms, self.update_interval_ms)
                self.update_interval_ms = min(
                    self.start_update_interval_ms, self.update_interval_ms)
            update_game_speed()

        return scored_rows

    def auto_move_down(self):
        if not self.moving_figure.moves_down():
            self._move_internal(Direction.down, self.update_interval_ms)
        self.moving_figure.update_position()

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
