from enum import Enum
import numpy
from FigureBuilder import FigureBuilder
from Figures import *
from Player import Player


class MoveResult(Enum):
    Nothing = 1
    HasMoved = 2
    HasSpawnedFigure = 3
    IsGameOver = 4


class Tetris:
    start_update_interval_ms: int = 500
    min_update_interval_ms: int = 150
    manual_movement_duration_ms: int = 50

    number_of_rows: int
    number_of_columns: int
    update_interval_ms: int
    field: numpy.ndarray
    moving_figure: Figure
    auto_move_time_counter: TimeCounter
    manual_move_time_counter: TimeCounter
    last_figure: Figure
    next_figure: Figure
    player: Player

    def __init__(self, number_of_rows: int, number_of_columns: int):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.next_figure = None
        self.moving_figure = None
        self.player = Player()
        self.manual_move_time_counter = TimeCounter(20)
        self._start_new_game()

    def spawn_figure(self, position: BlockPosition):
        if not self.next_figure:
            self.next_figure = FigureBuilder.random(position)

        self.last_figure = deepcopy(self.moving_figure)
        self.moving_figure = deepcopy(self.next_figure)
        self.next_figure = FigureBuilder.random(position)

    def _move_collides(self, figure: Figure, direction: Direction) -> bool:
        is_moving_down = figure.is_moving_down()
        is_moving_right = figure.is_moving_right()
        is_moving_left = figure.is_moving_left()

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
        self.update_interval_ms = self.start_update_interval_ms
        self.auto_move_time_counter = TimeCounter(self.update_interval_ms)
        self.player.reset()

    def _move_internal(self, direction: Direction, duration_ms: int) -> MoveResult:
        if not self._move_collides(self.moving_figure, direction):
            self.moving_figure.move(direction, duration_ms)
            return MoveResult.HasMoved

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
                return MoveResult.IsGameOver
            else:
                return MoveResult.HasSpawnedFigure
        else:
            return MoveResult.Nothing

    def move(self, direction: Direction) -> MoveResult:
        move_result = MoveResult.Nothing

        if self.manual_move_time_counter.is_elapsed():
            move_result = self._move_internal(
                direction, self.manual_movement_duration_ms)
            self.manual_move_time_counter.restart()
        self.moving_figure.update_position()

        return move_result

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
                self.auto_move_time_counter.update_duration(
                    self.update_interval_ms)
            update_game_speed()

        return scored_rows

    def auto_move_down(self) -> MoveResult:
        move_result = MoveResult.Nothing

        if not self.moving_figure.is_moving_down():
            if self.auto_move_time_counter.is_elapsed():
                move_result = self._move_internal(
                    Direction.down, self.manual_movement_duration_ms)
                self.auto_move_time_counter.restart()
        self.moving_figure.update_position()

        return move_result if (move_result is not move_result.Nothing) else MoveResult.HasMoved

    def get_last_figure(self) -> Figure:
        return self.last_figure

    def get_moving_figure(self) -> Figure:
        return self.moving_figure

    def get_next_figure(self) -> Figure:
        return self.next_figure
