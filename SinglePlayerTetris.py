
from SoundPlayer import SoundPlayer, Sound
from Tetris import MoveResult, Tetris
from View.TetrisPainter import TetrisPainter
from KeyPressHandler import KeyPressHandler
from Common import Direction, TimeCounter

import pygame


class SinglePlayerTetris:
    fps: int
    fps_clock: pygame.time.Clock
    is_running: bool
    sound_player: SoundPlayer
    long_press_direction_time_counter: TimeCounter
    is_rotation_key_pressed_before: bool
    number_of_offscreen_rows: int
    tetris_painter: TetrisPainter
    tetris: Tetris

    def __init__(self, fps: int = 120, long_press_delay_ms: int = 250):
        pygame.init()

        number_of_rows = 20
        number_of_columns = 10
        number_of_offscreen_rows = 2

        self.fps = fps
        self.fps_clock = pygame.time.Clock()
        self.is_running = True
        self.key_press_handler = KeyPressHandler()
        self.sound_player = SoundPlayer()
        self.long_press_direction_time_counter = TimeCounter(
            long_press_delay_ms)
        self.is_rotation_key_pressed_before = False
        self.tetris_painter = TetrisPainter(
            number_of_rows + number_of_offscreen_rows, number_of_columns, number_of_offscreen_rows)
        self.tetris = Tetris(
            number_of_rows + number_of_offscreen_rows, number_of_columns)

    def _draw_all(self):
        score = self.tetris.get_score()
        self.tetris_painter.draw_score(score)
        moving_figure = self.tetris.get_moving_figure()
        self.tetris_painter.draw_figure(moving_figure, True)
        next_figure = self.tetris.get_next_figure()
        self.tetris_painter.draw_figure_preview(next_figure)
        self.tetris_painter.redraw_all(self.tetris.field)

    def _handle_move_result(self, move_result: MoveResult):
        moving_figure = self.tetris.get_moving_figure()
        next_figure = self.tetris.get_next_figure()
        next_figure = self.tetris.get_next_figure()
        last_figure = self.tetris.get_last_figure()

        match move_result:
            case MoveResult.IsGameOver:
                self.sound_player.play_sound(Sound.gameover)
                self._draw_all()

            case MoveResult.HasSpawnedFigure:
                self.tetris_painter.draw_figure(last_figure, False)
                scored_rows = self.tetris.check_rows()
                number_of_scored_rows = len(scored_rows)
                if number_of_scored_rows > 0:
                    if number_of_scored_rows == 4:
                        self.sound_player.play_sound(Sound.clear_row_perfect)
                    else:
                        self.sound_player.play_sound(Sound.clear_row)

                    self.tetris_painter.color_rows(
                        scored_rows, last_figure.block_color)
                    self.fps_clock.tick(3)
                    score = self.tetris.get_score()
                    self.tetris_painter.draw_score(score)
                    self.tetris_painter.add_to_static_blocks(last_figure)
                    self.tetris_painter.draw_figure(moving_figure, True)
                    self.tetris_painter.redraw_all(self.tetris.field)
                else:
                    self.sound_player.play_sound(Sound.landing)
                    self.tetris_painter.draw_figure(moving_figure, True)
                self.tetris_painter.draw_figure_preview(next_figure)

            case MoveResult.HasMoved:
                self.sound_player.play_sound(Sound.move_figure)
                self.tetris_painter.draw_figure(moving_figure, False)

            case MoveResult.Nothing:
                self.tetris_painter.draw_figure(moving_figure, False)

    def _aggregate_move_results(self, move_result_list: list[MoveResult]):
        aggregated_move_result = MoveResult.Nothing
        for move_result in move_result_list:
            if move_result is MoveResult.IsGameOver:
                return MoveResult.IsGameOver
            elif move_result.value > aggregated_move_result.value:
                aggregated_move_result = move_result

        return aggregated_move_result

    def _handle_input(self) -> list[MoveResult]:
        self.key_press_handler.update_pressed_keys()
        if self.key_press_handler.is_quit_pressed():
            self.is_running = False
            return []

        move_results = []

        # Handle rotation
        is_rotation_key_pressed = self.key_press_handler.is_key_pressed(
            Direction.up)
        if is_rotation_key_pressed:
            if not self.is_rotation_key_pressed_before:
                move_result = self.tetris.move(Direction.up)
                move_results.append(move_result)
        self.is_rotation_key_pressed_before = is_rotation_key_pressed

        if not self.key_press_handler.is_any_direction_key_pressed():
            self.long_press_direction_time_counter.stop()
        else:
            # Handle movement
            for direction in [Direction.right, Direction.left, Direction.down]:
                if self.key_press_handler.is_key_pressed(direction):
                    # First registered key press
                    if not self.long_press_direction_time_counter.is_started():
                        self.long_press_direction_time_counter.start()
                        move_result = self.tetris.move(direction)
                        move_results.append(move_result)

                    # Long key press
                    elif self.long_press_direction_time_counter.is_elapsed():
                        # Disable for rotation, because it's annyoing
                        if direction != Direction.up:
                            move_result = self.tetris.move(direction)
                            move_results.append(move_result)

        return move_results

    def run(self):
        self.sound_player.play_theme()
        self._draw_all()

        while self.is_running:
            frame_move_results = self._handle_input()
            move_result = self.tetris.auto_move_down()
            frame_move_results.append(move_result)
            aggregated_move_result = self._aggregate_move_results(
                frame_move_results)
            self._handle_move_result(aggregated_move_result)
            self.fps_clock.tick(self.fps)
        pygame.quit()
