
import pygame
from Tetris import MoveResult, Tetris
from View.TetrisPainter import TetrisPainter
from KeyPressHandler import KeyPressHandler
from Common import Direction, TimeCounter

pygame.init()

fps = 120
fpsClock = pygame.time.Clock()
key_press_handler = KeyPressHandler()
running = True
long_press_direction_time_counter = TimeCounter(150)
is_rotation_key_pressed_before = False

number_of_offscreen_rows = 2
tetris = Tetris(20 + number_of_offscreen_rows, 10)
tetris_painter = TetrisPainter(
    tetris.number_of_rows, tetris.number_of_columns, number_of_offscreen_rows)


def draw_on_update(move_result: MoveResult):
    moving_figure = tetris.get_moving_figure()
    next_figure = tetris.get_next_figure()
    last_figure = tetris.get_last_figure()

    match move_result:
        case MoveResult.IsGameOver:
            tetris_painter.draw_score(tetris.player.score)
            tetris_painter.draw_figure(moving_figure, True)
            tetris_painter.draw_figure_preview(next_figure)
            tetris_painter.redraw_all(tetris.field)

        case MoveResult.HasSpawnedFigure:
            tetris_painter.draw_figure(last_figure, False)
            scored_rows = tetris.check_rows()
            if len(scored_rows) > 0:
                tetris_painter.color_rows(scored_rows, last_figure.block_color)
                fpsClock.tick(3)
                tetris_painter.draw_score(tetris.player.score)
                tetris_painter.add_to_static_blocks(last_figure)
                tetris_painter.draw_figure(moving_figure, True)
                tetris_painter.redraw_all(tetris.field)
            else:
                tetris_painter.draw_figure(moving_figure, True)
            tetris_painter.draw_figure_preview(next_figure)

        case MoveResult.HasMoved:
            tetris_painter.draw_figure(moving_figure, False)

        case MoveResult.Nothing:
            pass


draw_on_update(MoveResult.IsGameOver)

while running:
    key_press_handler.update_pressed_keys()
    if key_press_handler.is_quit_pressed():
        running = False

    # Handle rotation
    is_rotation_key_pressed = key_press_handler.is_key_pressed(Direction.up)
    if is_rotation_key_pressed:
        if not is_rotation_key_pressed_before:
            move_result = tetris.move(Direction.up)
            draw_on_update(move_result)
    is_rotation_key_pressed_before = is_rotation_key_pressed

    # Handle movement
    for direction in [Direction.right, Direction.left, Direction.down]:
        if key_press_handler.is_key_pressed(direction):
            # First registered key press
            if not long_press_direction_time_counter.is_started():
                long_press_direction_time_counter.start()
                move_result = tetris.move(direction)
                draw_on_update(move_result)
            # Long key press
            elif long_press_direction_time_counter.is_elapsed():
                # Long key press is kinda annoying for rotating the figure.
                if direction != Direction.up:
                    move_result = tetris.move(direction)
                    draw_on_update(move_result)

    if not key_press_handler.is_any_direction_key_pressed():
        long_press_direction_time_counter.stop()

    move_result = tetris.auto_move_down()
    draw_on_update(move_result)
    fpsClock.tick(fps)

pygame.quit()
