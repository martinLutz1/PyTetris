
import pygame
import time
from Tetris import Tetris
from TetrisPainter import TetrisPainter
from KeyPressHandler import KeyPressHandler
from Common import Direction

pygame.init()
tetris = Tetris(20, 10)
tetris_painter = TetrisPainter(
    400, 800, tetris.number_of_rows, tetris.number_of_columns)

fps = 60
fpsClock = pygame.time.Clock()

key_press_handler = KeyPressHandler()
ms_until_long_press = 150
ms_elapsed_since_last_key_down = 0

running = True
while running:
    key_press_handler.update_pressed_keys()

    if key_press_handler.is_quit_pressed:
        running = False

    is_new_figure_spawned = False

    for direction in [Direction.RIGHT, Direction.LEFT, Direction.DOWN, Direction.UP]:
        if key_press_handler.is_direction_key_pressed[direction.value]:
            ms_elapsed_now = time.time() * 1000
            # First registered key press
            if ms_elapsed_since_last_key_down == 0:
                ms_elapsed_since_last_key_down = ms_elapsed_now
                if tetris.move(direction):
                    is_new_figure_spawned = True
            # Long key press
            elif (ms_elapsed_now - ms_elapsed_since_last_key_down) >= ms_until_long_press:
                if tetris.move(direction):
                    is_new_figure_spawned = True

    if not (True in key_press_handler.is_direction_key_pressed):
        ms_elapsed_since_last_key_down = 0

    if tetris.update():
        is_new_figure_spawned = True

    # Scored, rows were deleted -> redraw
    if is_new_figure_spawned and tetris.check_rows():
        tetris_painter.redraw_all(tetris.field)
    else:
        tetris_painter.draw_figure(tetris.moving_figure, is_new_figure_spawned)

    fpsClock.tick(fps)

pygame.quit()
