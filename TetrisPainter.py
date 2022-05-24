import pygame
from Figures import Figure
from typing import List
from Common import Direction
from pygame import gfxdraw


def draw_rounded_rect(surface, rect, color, corner_radius):
    ''' Draw a rectangle with rounded corners.
    Would prefer this: 
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    but this option is not yet supported in my version of pygame so do it ourselves.

    We use anti-aliased circles to make the corners smoother
    '''
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(
            f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius,
                            rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1,
                            rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius,
                            rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1,
                            rect.bottom-corner_radius-1, corner_radius, color)

    pygame.gfxdraw.filled_circle(
        surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(
        surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(
        surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(
        surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)


def draw_bordered_rounded_rect(surface, rect, color, border_color, corner_radius, border_thickness):
    if corner_radius < 0:
        raise ValueError(f"border radius ({corner_radius}) must be >= 0")

    rect_tmp = pygame.Rect(rect)
    center = rect_tmp.center

    if border_thickness:
        if corner_radius <= 0:
            pygame.draw.rect(surface, border_color, rect_tmp)
        else:
            draw_rounded_rect(surface, rect_tmp, border_color, corner_radius)

        rect_tmp.inflate_ip(-2*border_thickness, -2*border_thickness)
        inner_radius = corner_radius - border_thickness + 1
    else:
        inner_radius = corner_radius

    if inner_radius <= 0:
        pygame.draw.rect(surface, color, rect_tmp)
    else:
        draw_rounded_rect(surface, rect_tmp, color, inner_radius)


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
            draw_bordered_rounded_rect(self.screen,
                                       pygame.Rect(getScreenPositionX(point.x), getScreenPositionY(point.y), self.figure_width, self.figure_height), figure.color, (30, 30, 30), 10, 5)

    def draw(self, figures: List[Figure], number_of_rows: int, number_of_columns: int):
        self.screen.fill((255, 255, 255))

        for figure in figures:
            self._draw_figure(figure)

        pygame.display.flip()
        pygame.display.update()
