
from Figures import BlockColor, BlockPosition, Figure, Offset
from View.FigureSprite import FigureSprite
from View.ViewCommon import *
from View.BlockView import TetrisBlockView

from copy import deepcopy
import numpy
import pygame


class TetrisView:
    border_thickness: int = 20

    x_position: int
    y_position: int
    tetris_area_x_position: int
    tetris_area_width: int
    width: int
    height: int
    number_of_rows: int
    number_of_columns: int
    number_of_offscreen_rows: int
    surface: pygame.Surface
    figure_sprite: FigureSprite
    static_block_views: list[TetrisBlockView]
    view_description: ViewDescription
    block_description: BlockDescription

    def __init__(self, x_position: int, y_position: int, width: int, height: int,
                 number_of_rows: int, number_of_columns: int, number_of_offscreen_rows: int,
                 view_description: ViewDescription):
        self.x_position = x_position
        self.y_position = y_position
        self.tetris_area_x_position = x_position + self.border_thickness
        self.tetris_area_width = width - 2 * self.border_thickness
        self.width = width
        self.height = height
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.number_of_offscreen_rows = number_of_offscreen_rows
        self.surface = pygame.Surface((width, height))
        self.static_block_views = []
        self.view_description = view_description

        # Init block description
        block_width = self.tetris_area_width / number_of_columns
        block_height = height / (number_of_rows - number_of_offscreen_rows)
        block_border_thickness = int(block_width / 8)
        self.block_description = BlockDescription(
            block_width, block_height, block_border_thickness)

    def _draw_border(self, x_position: int):
        border_rect = pygame.Rect(
            x_position, self.y_position, self.border_thickness, self.view_description.screen_height)

        pygame.draw.rect(self.surface, border_color, border_rect)

    def _get_block_view(self, color: pygame.Color, position: BlockPosition,
                        offset: Offset = Offset(0, 0)) -> TetrisBlockView:
        block_position = BlockPosition(
            position.x, position.y - self.number_of_offscreen_rows)
        return TetrisBlockView(self.block_description, block_position, offset, color)

    def _get_block_views(self, figure: Figure) -> list[TetrisBlockView]:
        block_views = []

        for block in figure.get_blocks():
            block_view = self._get_block_view(
                figure.block_color, block, figure.offset)
            block_views.append(block_view)

        return block_views

    def _draw_block_views(self, block_views: list[TetrisBlockView]) -> list[pygame.Rect]:
        updated_rects = []

        for block_view in block_views:
            if block_view.position.y >= -1:
                drawn_rect = block_view.draw(self.surface)
                updated_rects.append(drawn_rect)

        return self._to_absolute_position(updated_rects)

    def _to_absolute_position(self, rects: list[pygame.Rect]) -> list[pygame.Rect]:
        updated_rects = deepcopy(rects)
        for rect in updated_rects:
            rect.x += self.tetris_area_x_position
            rect.y += self.y_position
        return updated_rects

    def add_to_static_blocks(self, figure: Figure):
        self.static_block_views.extend(self._get_block_views(figure))

    def set_moving_figure(self, figure: Figure):
        self.figure_sprite = None
        self.figure_sprite = FigureSprite(
            figure, self.block_description, self.number_of_offscreen_rows, tetris_bg_color, self.border_thickness)

    def update_figure_position(self, figure: Figure):
        self.figure_sprite.update_position(figure)

    def set_static_blocks(self, field: numpy.ndarray):
        self.static_block_views.clear()

        for y in range(field.shape[0]):
            for x in range(field.shape[1]):
                if field[y][x]:
                    block_view = self._get_block_view(
                        field[y][x], BlockPosition(x, y))
                    self.static_block_views.append(block_view)

    def blit(self, parent_surface: pygame.Surface):
        parent_surface.blit(
            self.surface, (self.tetris_area_x_position, self.y_position))

    def clear_moving_figure(self) -> list[pygame.Rect]:
        updated_rects = self.figure_sprite.clear(self.surface)
        return self._to_absolute_position(updated_rects)

    def draw_moving_figure(self) -> list[pygame.Rect]:
        updated_rects = self.figure_sprite.draw(self.surface)
        return self._to_absolute_position(updated_rects)

    def color_rows(self, rows: list[int], block_color: BlockColor,
                   parent_surface: pygame.surface) -> list[pygame.Rect]:

        def get_block_views_for_row(row: int) -> list[TetrisBlockView]:
            block_views = []

            for x in range(self.number_of_columns):
                block_view = self._get_block_view(
                    block_color, BlockPosition(x, row))
                block_views.append(block_view)

            return block_views

        updated_rects = []

        for row in rows:
            row_block_views = get_block_views_for_row(row)
            block_rects = self._draw_block_views(row_block_views)
            updated_rects.extend(block_rects)
        self.blit(parent_surface)

        return updated_rects

    def draw_all(self, parent_surface: pygame.surface):
        self.surface.fill(tetris_bg_color)
        self._draw_border(0)
        self._draw_border(self.border_thickness + self.tetris_area_width)
        self._draw_block_views(self.static_block_views)
        self.figure_sprite.draw(parent_surface)
        self.blit(parent_surface)
