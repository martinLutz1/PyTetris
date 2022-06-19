

from copy import deepcopy
import pygame
from Figures import Figure
from View.BlockView import BlockView
from View.ViewCommon import BlockDescription


class FigurePreviewView:
    x_position: int
    y_position: int
    block_description: BlockDescription
    background_color: pygame.Color
    figure: Figure
    last_drawn_rects: list[pygame.Rect]

    def __init__(self, x_position: int, y_position: int, block_description: BlockDescription,
                 background_color: pygame.Color):
        self.x_position = x_position
        self.y_position = y_position
        self.block_description = block_description
        self.background_color = background_color
        self.figure = None
        self.last_drawn_rects = []

    def update_figure(self, figure: Figure):
        self.figure = deepcopy(figure)

    def draw(self, parent_surface: pygame.Surface):
        if not self.figure:
            return []

        self.last_drawn_rects.clear()

        for block in self.figure.get_static_blocks():
            x_position = self.x_position + block.x * self.block_description.width
            y_position = self.y_position + block.y * self.block_description.height
            block_view = BlockView(
                x_position, y_position, self.block_description, self.figure.block_color)
            block_rect = block_view.draw(parent_surface)
            self.last_drawn_rects.append(block_rect)

        return self.last_drawn_rects

    def clear(self, parent_surface: pygame.Surface) -> list[pygame.Rect]:
        for rect in self.last_drawn_rects:
            parent_surface.fill(self.background_color, rect)
        return self.last_drawn_rects
