from Figures import Figure
from View.BlockView import BlockView
from View.DrawSupport import draw_frame
from View.TextView import TextView
from View.ViewCommon import *

from copy import deepcopy
import pygame


class FigurePreviewView:
    text: str = "Next"

    x_position: int
    y_position: int
    block_description: BlockDescription
    figure: Figure
    last_drawn_rects: list[pygame.Rect]
    headline: TextView
    frame_rect: pygame.Rect

    def __init__(self, x_position: int, y_position: int, block_description: BlockDescription):
        self.x_position = x_position
        self.y_position = y_position
        self.block_description = block_description
        self.figure = None
        self.last_drawn_rects = []

        # Init headline
        self.headline = TextView(
            medium_font, text_color, x_position, y_position)
        self.headline.update_text(self.text)

        # Init frame
        frame_width = 4 * self.block_description.width
        frame_height = 5 * self.block_description.width
        frame_y_position = y_position + medium_font_height
        self.frame_rect = pygame.Rect(
            x_position, frame_y_position, frame_width, frame_height)

    def update_figure(self, figure: Figure):
        self.figure = deepcopy(figure)

    def draw(self, parent_surface: pygame.Surface) -> list[pygame.Rect]:
        if not self.figure:
            return []

        self.last_drawn_rects.clear()
        self.headline.draw(parent_surface)

        draw_frame(parent_surface, self.frame_rect, self.block_description)
        self.last_drawn_rects.append(self.frame_rect)

        offset = self.figure.get_static_offset()
        for block in self.figure.get_static_blocks():
            x_position = self.frame_rect.x + \
                (block.x + 1 + offset.x) * self.block_description.width
            y_position = self.frame_rect.y + \
                (block.y + 0.5 + offset.y) * self.block_description.height
            block_view = BlockView(
                x_position, y_position, self.block_description, self.figure.block_color)
            block_view.draw(parent_surface)

        return [self.frame_rect]
