import pygame
from Figures import Figure
from typing import List
from Common import Direction


class TetrisPainter:
    screen_width: int
    screen_height: int
    figure_width: int
    figure_height: int
    screen: pygame.Surface

    def __init__(self, screen_width: int, screen_height: int, number_of_rows: int, number_of_columns: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.figure_width = screen_width / number_of_columns
        self.figure_height = screen_height / number_of_rows
        self.screen = pygame.display.set_mode([screen_width, screen_height])

    def _draw_figure(self, figure: Figure):
        def getScreenPositionX(xPosition):
            return xPosition * \
                (self.screen_width / self.number_of_columns)

        def getScreenPositionY(yPosition):
            return yPosition * \
                (self.screen_height / self.number_of_rows)

        for point in figure.get_used_points():
            pygame.draw.rect(self.screen, (0, 0, 255),
                             pygame.Rect(getScreenPositionX(point.x), getScreenPositionY(point.y), self.figure_width, self.figure_height), 75)

    def draw(self, figures: List[Figure], number_of_rows: int, number_of_columns: int):
        self.screen.fill((255, 255, 255))

        for figure in figures:
            self._draw_figure(figure)

        pygame.display.flip()
        pygame.display.update()
