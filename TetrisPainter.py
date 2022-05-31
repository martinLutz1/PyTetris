from copy import deepcopy
import numpy
import pygame
from typing import List, Optional

from Figures import BlockColor, Figure, Position
from DrawSupport import *
from TextWall import TextWall


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

    def __init__(self, screen_width: int, screen_height: int, tetris_width: int, x_screen_offset: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tetris_width = tetris_width
        self.x_screen_offset = x_screen_offset


class TetrisDescription:
    number_of_rows: int
    number_of_columns: int
    number_of_offscreen_rows: int

    def __init__(self, number_of_rows: int, number_of_columns: int, number_of_offscreen_rows: int):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.number_of_offscreen_rows = number_of_offscreen_rows


class Score:
    color: pygame.Color = (40, 40, 40)
    max_screen_distance: int = 10

    font: pygame.font.Font
    text_wall: TextWall

    def __init__(self, screen: pygame.Surface, screen_width: int, screen_height: int):
        self.font = pygame.font.Font("Font/OpenDyslexic3-Regular.ttf", 50)

        def get_score_position():
            y_score_position_candidate = int(screen_height * 0.05)
            y_score_position = self.max_screen_distance if (
                y_score_position_candidate > Score.max_screen_distance) else y_score_position_candidate

            x_score_position_candidate = int(screen_width * 0.95)
            x_score_position = screen_width - self.max_screen_distance if (
                (screen_width - x_score_position_candidate) > Score.max_screen_distance) else x_score_position_candidate
            score_width, score_height = self.font.size(self._get_score_text(0))

            return Position(x_score_position - score_width, y_score_position + score_height)

        self.text_wall = TextWall(
            self.font, self.color, get_score_position(), screen)

    def _get_score_text(self, score: int):
        return "Score: " + str(score)

    def update(self, score: int):
        self.text_wall.update_text(self._get_score_text(score))

    def draw(self):
        self.text_wall.draw()


class Background:
    color: pygame.Color = (50, 50, 50)
    unused_area_color:  pygame.Color = (150, 150, 150)
    border_color: pygame.Color = (40, 40, 40)
    border_thickness: int = 20

    view_description: ViewDescription
    tetris_description: TetrisDescription
    block_description: BlockDescription

    def __init__(self, view_description: ViewDescription, tetris_description: TetrisDescription,
                 block_description: BlockDescription):
        self.view_description = view_description
        self.tetris_description = tetris_description
        self.block_description = block_description

    def _draw_border(self, surface: pygame.Surface, x_position: int):
        border_rect = pygame.Rect(
            x_position, 0, self.border_thickness, self.view_description.screen_height)
        pygame.draw.rect(surface, self.border_color, border_rect)

    def _draw_unused_area(self, surface: pygame.Surface, x_position: int):
        rect_width = self.view_description.x_screen_offset - self.border_thickness
        border_rect = pygame.Rect(
            x_position, 0, rect_width, self.view_description.screen_height)
        pygame.draw.rect(surface, self.unused_area_color, border_rect)

    def draw(self, surface: pygame.Surface):
        surface.fill(self.color)

        # Left area
        self._draw_border(
            surface, self.view_description.x_screen_offset - self.border_thickness)
        self._draw_unused_area(surface, 0)

        # Right area
        self._draw_border(surface, self.view_description.screen_width -
                          self.view_description.x_screen_offset)
        self._draw_unused_area(surface, self.view_description.screen_width -
                               self.view_description.x_screen_offset + self.border_thickness)


class TetrisPainter:
    screen: pygame.Surface
    view_description: ViewDescription
    block_description: BlockDescription
    tetris_description: TetrisDescription
    score: Score
    background: Background
    last_drawn_figure: Optional[Figure] = None

    def __init__(self, number_of_rows: int, number_of_columns: int, number_of_offscreen_rows: int):
        screen_width = pygame.display.Info().current_w
        screen_height = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height), pygame.FULLSCREEN)

        tetris_area_width = screen_height / 2
        x_screen_offset = (screen_width - tetris_area_width) / 2
        self.view_description = ViewDescription(
            screen_width, screen_height, tetris_area_width, x_screen_offset)

        block_width = tetris_area_width / number_of_columns
        block_height = screen_height / \
            (number_of_rows - number_of_offscreen_rows)
        block_border_thickness = int(block_width / 8)
        self.block_description = BlockDescription(
            block_width, block_height, block_border_thickness)

        self.tetris_description = TetrisDescription(
            number_of_rows, number_of_columns, number_of_offscreen_rows)

        self.score = Score(self.screen, screen_width, screen_height)
        self.background = Background(
            self.view_description, self.tetris_description, self.block_description)

        self.background.draw(self.screen)
        self.score.update(0)

    def _get_screen_position_x(self, x_position):
        return x_position * self.block_description.width + self.view_description.x_screen_offset

    def _get_screen_position_y(self, y_position):
        return (y_position - self.tetris_description.number_of_offscreen_rows) * self.block_description.height

    def _draw_block(self, position: Position, block_color: BlockColor) -> pygame.Rect:
        if position.y < self.tetris_description.number_of_offscreen_rows - 1:
            return

        block_rect = pygame.Rect(self._get_screen_position_x(position.x),
                                 self._get_screen_position_y(position.y),
                                 self.block_description.width,
                                 self.block_description.height)
        draw_bordered_rounded_rect(self.screen, deepcopy(block_rect), block_color.body_color,
                                   block_color.border_color, 10, self.block_description.border_thickness)
        return block_rect

    def _clear_last_figure(self) -> List[pygame.Rect]:
        if self.last_drawn_figure.position.y < self.tetris_description.number_of_offscreen_rows - 1:
            return []
        if self.last_drawn_figure == None:
            return []

        updated_rects = []
        for block in self.last_drawn_figure.get_blocks():
            block_rect = pygame.Rect(self._get_screen_position_x(block.x),
                                     self._get_screen_position_y(block.y),
                                     self.block_description.width,
                                     self.block_description.height)
            pygame.draw.rect(
                self.screen, self.background.color, block_rect)
            updated_rects.append(block_rect)
        return updated_rects

    def _draw_figure(self, figure: Figure):
        updated_rects = []
        for block in figure.get_blocks():
            drawn_rect = self._draw_block(block, figure.block_color)
            updated_rects.append(drawn_rect)
        return updated_rects

    def draw_figure(self, figure: Figure, is_new_figure: bool):
        if figure is self.last_drawn_figure:
            return

        updated_rects = []
        if not is_new_figure:
            cleared_rects = self._clear_last_figure()
            updated_rects.extend(cleared_rects)

        drawn_rects = self._draw_figure(figure)
        updated_rects.extend(drawn_rects)

        pygame.display.update(updated_rects)
        self.last_drawn_figure = deepcopy(figure)

    def redraw_all(self, field: numpy.ndarray, figure: Figure):
        self.background.draw(self.screen)
        self._draw_figure(figure)
        self.last_drawn_figure = deepcopy(figure)

        for y in range(field.shape[0]):
            for x in range(field.shape[1]):
                if field[y][x]:
                    self._draw_block(Position(x, y), field[y, x])

        self.score.draw()
        pygame.display.update()

    def color_rows(self, rows: List[int], block_color: BlockColor):
        updated_rects = []
        for y in rows:
            for x in range(self.tetris_description.number_of_columns):
                drawn_rect = self._draw_block(Position(x, y), block_color)
                updated_rects.append(drawn_rect)
        pygame.display.update(updated_rects)
