
import pygame
from Tetris import Tetris
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
tetris_painter.draw_figure(tetris.moving_figure, True)
tetris_painter.redraw_all(tetris.field)


def draw_on_update():
    if tetris.is_game_over():
        tetris_painter.draw_score(tetris.player.score)
        tetris_painter.draw_figure(tetris.moving_figure, True)
        tetris_painter.redraw_all(tetris.field)

    elif tetris.has_spawned_figure():
        scored_rows = tetris.check_rows()
        if len(scored_rows) > 0:
            tetris_painter.draw_figure(tetris.last_figure, False)
            tetris_painter.color_rows(
                scored_rows, tetris_painter.last_figure.block_color)
            fpsClock.tick(3)
            tetris_painter.draw_score(tetris.player.score)
            tetris_painter.draw_figure(tetris.moving_figure, True)
            tetris_painter.redraw_all(tetris.field)
        else:
            if tetris.last_figure:
                tetris_painter.draw_figure(tetris.last_figure, False)
            tetris_painter.draw_figure(tetris.moving_figure, True)
    else:
        tetris_painter.draw_figure(tetris.moving_figure, False)


while running:
    key_press_handler.update_pressed_keys()
    if key_press_handler.is_quit_pressed():
        running = False

    # Handle rotation
    is_rotation_key_pressed = key_press_handler.is_key_pressed(Direction.up)
    if is_rotation_key_pressed:
        if not is_rotation_key_pressed_before:
            tetris.move(Direction.up)
    is_rotation_key_pressed_before = is_rotation_key_pressed

    # Handle movement
    for direction in [Direction.right, Direction.left, Direction.down]:
        if key_press_handler.is_key_pressed(direction):
            # First registered key press
            if not long_press_direction_time_counter.is_started():
                long_press_direction_time_counter.start()
                tetris.move(direction)
            # Long key press
            elif long_press_direction_time_counter.is_elapsed():
                # Long key press is kinda annoying for rotating the figure.
                if direction != Direction.up:
                    tetris.move(direction)

    if not key_press_handler.is_any_direction_key_pressed():
        long_press_direction_time_counter.stop()

    tetris.auto_move_down()
    draw_on_update()
    fpsClock.tick(fps)

pygame.quit()
