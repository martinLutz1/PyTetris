from copy import deepcopy
import numpy
import pygame
from Figures import BlockColor, Figure, Position
from typing import List, Optional
from pygame import gfxdraw, Color


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

    if border_thickness:
        if corner_radius <= 0:
            pygame.draw.rect(surface, border_color, rect)
        else:
            draw_rounded_rect(surface, rect, border_color, corner_radius)

        rect.inflate_ip(-2*border_thickness, -2*border_thickness)
        inner_radius = corner_radius - border_thickness + 1
    else:
        inner_radius = corner_radius

    if inner_radius <= 0:
        pygame.draw.rect(surface, color, rect)
    else:
        draw_rounded_rect(surface, rect, color, inner_radius)


class BlockDescription:
    height: int
    width: int
    border_thickness: int

    def __init__(self, width: int, height: int, border_thickness: int):
        self.width = width
        self.height = height
        self.border_thickness = border_thickness


class ViewDescription:
    screen_width: int
    screen_height: int
    tetris_width: int
    x_screen_offset: int
    score_position: Position

    def __init__(self, screen_width: int, screen_height: int, tetris_width: int,
                 x_screen_offset: int, score_position: Position):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tetris_width = tetris_width
        self.x_screen_offset = x_screen_offset
        self.score_position = score_position


class TetrisPainter:
    view: ViewDescription
    block_description: BlockDescription
    screen: pygame.Surface
    background_color: pygame.Color = (255, 255, 255)
    last_drawn_figure: Optional[Figure] = None
    font: pygame.font.Font
    number_of_rows: int
    number_of_columns: int

    def __init__(self, number_of_rows: int, number_of_columns: int):
        screen_width = pygame.display.Info().current_w
        screen_height = pygame.display.Info().current_h
        tetris_area_width = screen_height / 2
        x_screen_offset = (screen_width - tetris_area_width) / 2
        score_position = screen_width - 140, 60
        self.view = ViewDescription(
            screen_width, screen_height, tetris_area_width, x_screen_offset, score_position)

        block_width = tetris_area_width / number_of_columns
        block_height = tetris_area_width / number_of_columns
        block_border_thickness = int(block_width / 8)
        self.block_description = BlockDescription(
            block_width, block_height, block_border_thickness)

        self.screen = pygame.display.set_mode(
            [screen_width, screen_height], pygame.FULLSCREEN)
        self.font = pygame.font.Font("Font/OpenDyslexic3-Regular.ttf", 32)

        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns

        self._draw_background()

    def _draw_background(self):
        self.screen.fill(self.background_color)
        border_thickness = 20  # self.view.x_screen_offset
        border_color = pygame.Color(100, 100, 100)

        # Left border
        x_left = self.view.x_screen_offset - border_thickness
        pygame.draw.rect(
            self.screen,
            border_color,
            pygame.Rect(x_left, 0, border_thickness, self.view.screen_height))

        # Right border
        x_right = self.view.screen_width - self.view.x_screen_offset
        pygame.draw.rect(
            self.screen,
            border_color,
            pygame.Rect(x_right, 0, border_thickness, self.view.screen_height))

    def _get_screen_position_x(self, xPosition):
        return xPosition * (self.view.tetris_width / self.number_of_columns) + self.view.x_screen_offset

    def _get_screen_position_y(self, yPosition):
        return yPosition * (self.view.screen_height / self.number_of_rows)

    def _draw_block(self, position: Position, block_color: BlockColor):
        draw_bordered_rounded_rect(
            self.screen,
            pygame.Rect(self._get_screen_position_x(position.x),
                        self._get_screen_position_y(position.y),
                        self.block_description.width,
                        self.block_description.height),
            block_color.body_color,
            block_color.border_color,
            10,
            self.block_description.border_thickness)

    def _clear_last_figure(self):
        if self.last_drawn_figure != None:
            for point in self.last_drawn_figure.get_used_points():
                pygame.draw.rect(
                    self.screen,
                    self.background_color,
                    pygame.Rect(self._get_screen_position_x(point.x),
                                self._get_screen_position_y(point.y),
                                self.block_description.width,
                                self.block_description.height))

    def _draw_figure(self, figure: Figure):
        for point in figure.get_used_points():
            self._draw_block(point, figure.block_color)

    def draw_score(self, score: int):
        score_as_string = "Score: " + str(score)

        text_surface = self.font.render(
            score_as_string, True, (30, 30, 30))
        text_rect = text_surface.get_rect(center=self.view.score_position)
        self.screen.blit(text_surface, text_rect)

    def draw_figure(self, figure: Figure, is_new_figure: bool):
        if figure is self.last_drawn_figure:
            return

        if not is_new_figure:
            self._clear_last_figure()
        self._draw_figure(figure)
        self.last_drawn_figure = deepcopy(figure)

    def redraw_all(self, field: numpy.ndarray, figure: Figure):
        self._draw_background()
        self._draw_figure(figure)
        self.last_drawn_figure = deepcopy(figure)

        for y in range(field.shape[0]):
            for x in range(field.shape[1]):
                if field[y][x]:
                    self._draw_block(Position(x, y), field[y, x])

    def update(self):
        pygame.display.flip()
        pygame.display.update()
