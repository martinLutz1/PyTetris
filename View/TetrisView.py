from copy import deepcopy
import numpy

import pygame
from Figures import BlockColor, BlockPosition, Figure, Offset
from View.FigureSprite import FigureSprite
from View.ViewCommon import BlockDescription
from View.BlockView import BlockView


class TetrisView:
    number_of_rows: int
    number_of_columns: int
    number_of_offscreen_rows: int
    surface: pygame.Surface
    block_description: BlockDescription
    x_position: int
    y_position: int
    figure_sprite: FigureSprite
    static_block_views: list[BlockView] = []
    background_color: pygame.Color = (50, 50, 50)

    def __init__(self, width: int, height: int, x_position: int, y_position: int,
                 number_of_rows: int, number_of_columns: int, number_of_offscreen_rows: int):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.number_of_offscreen_rows = number_of_offscreen_rows
        self.surface = pygame.Surface((width, height))
        block_width = width / number_of_columns
        block_height = height / (number_of_rows - number_of_offscreen_rows)
        block_border_thickness = int(block_width / 8)
        self.block_description = BlockDescription(
            block_width, block_height, block_border_thickness)
        self.x_position = x_position
        self.y_position = y_position

    def _get_block_view(self, color: pygame.Color, position: BlockPosition,
                        offset: Offset = Offset(0, 0)) -> BlockView:
        block_position = BlockPosition(
            position.x, position.y - self.number_of_offscreen_rows)
        return BlockView(self.block_description, block_position, offset, color)

    def _get_block_views(self, figure: Figure) -> list[BlockView]:
        block_views = []

        for block in figure.get_blocks():
            block_view = self._get_block_view(
                figure.block_color, block, figure.offset)
            block_views.append(block_view)

        return block_views

    def _draw_block_views(self, block_views: list[BlockView]) -> list[pygame.Rect]:
        updated_rects = []

        for block_view in block_views:
            if block_view.position.y >= -1:
                drawn_rect = block_view.draw(self.surface)
                drawn_rect.x += self.x_position
                drawn_rect.y += self.y_position
                updated_rects.append(drawn_rect)

        return updated_rects

    def _to_absolute_position(self, rects: list[pygame.Rect]) -> list[pygame.Rect]:
        for rect in rects:
            rect.x += self.x_position
            rect.y += self.y_position
        return rects

    def add_to_static_blocks(self, figure: Figure):
        self.static_block_views.extend(self._get_block_views(figure))

    def set_moving_figure(self, figure: Figure):
        self.figure_sprite = FigureSprite(
            figure, self.block_description, self.number_of_offscreen_rows, self.background_color)

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
        parent_surface.blit(self.surface, (self.x_position, self.y_position))

    def clear_moving_figure(self) -> list[pygame.Rect]:
        updated_rects = self.figure_sprite.clear(self.surface)
        return self._to_absolute_position(updated_rects)

    def draw_moving_figure(self) -> list[pygame.Rect]:
        updated_rects = self.figure_sprite.draw(self.surface)
        return self._to_absolute_position(updated_rects)

    def color_rows(self, rows: list[int], block_color: BlockColor,
                   parent_surface: pygame.surface) -> list[pygame.Rect]:

        def get_block_views_for_row(row: int) -> list[BlockView]:
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
        self.surface.fill(self.background_color)
        self._draw_block_views(self.static_block_views)
        self.figure_sprite.draw(parent_surface)
        self.blit(parent_surface)
