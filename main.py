
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

fps = 40
fpsClock = pygame.time.Clock()

key_press_handler = KeyPressHandler()
ms_until_long_press = 150
ms_elapsed_since_last_key_down = 0

running = True
while running:
    key_press_handler.update_pressed_keys()

    if key_press_handler.is_quit_pressed:
        running = False

    for direction in [Direction.RIGHT, Direction.LEFT, Direction.DOWN, Direction.UP]:
        if key_press_handler.is_direction_key_pressed[direction.value]:
            ms_elapsed_now = time.time() * 1000
            if ms_elapsed_since_last_key_down == 0:
                ms_elapsed_since_last_key_down = ms_elapsed_now
                tetris.move(direction)

            if (ms_elapsed_now - ms_elapsed_since_last_key_down) >= ms_until_long_press:
                tetris.move(direction)

    if not (True in key_press_handler.is_direction_key_pressed):
        ms_elapsed_since_last_key_down = 0

    tetris.update()
    tetris_painter.draw(tetris.figures, tetris.number_of_rows,
                        tetris.number_of_columns)
    fpsClock.tick(fps)

pygame.quit()
