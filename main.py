from enum import Enum
from tkinter.tix import DirSelectBox
from typing import List
import pygame
import numpy


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Position:
    x: int
    y: int


class Figure:
    position: Position
    directions: list

    def __init__(self, position, directions):
        self.position = position
        self.directions = directions


class FigureBuilder:
    class FigureType(Enum):
        I = 0
        O = 1
        T = 2
        S = 3
        Z = 4
        J = 5
        L = 6

    def new(position, figure_type) -> Figure:
        match figure_type:
            case FigureBuilder.FigureType.I:
                return Figure(position, [Direction.DOWN, Direction.DOWN, Direction.DOWN])
            case FigureBuilder.FigureType.O:
                return Figure(position, [Direction.DOWN, Direction.RIGHT, Direction.UP])
            case FigureBuilder.FigureType.I:
                return Figure(position, [Direction.DOWN, Direction.DOWN, Direction.DOWN])
            case FigureBuilder.FigureType.L:
                return Figure(position, [Direction.DOWN, Direction.DOWN, Direction.RIGHT])


def create_figure():
    return Figure()


class Tetris:
    number_of_rows: int
    number_of_columns: int
    field: numpy.ndarray
    figures: list

    def _init_figures(self):
        self.figures.append(Figure())

    def __init__(self, number_of_rows, number_of_columns):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.field = numpy.full((number_of_rows, number_of_columns), False)

        self._init_figures()

    def spawn_figure(self):

        # Import and initialize the pygame library
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
