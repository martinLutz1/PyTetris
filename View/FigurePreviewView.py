

from copy import deepcopy
import pygame
from Figures import Figure
from View.BlockView import BlockView
from View.DrawSupport import draw_bordered_rounded_rect, draw_frame
from View.TextView import TextView
from View.ViewCommon import BlockDescription


class FigurePreviewView:
    color: pygame.Color = (40, 40, 40)
    x_position: int
    y_position: int
    block_description: BlockDescription
    background_color: pygame.Color
    figure: Figure
    last_drawn_rects: list[pygame.Rect]
    headline: TextView

    def __init__(self, x_position: int, y_position: int, block_description: BlockDescription,
                 background_color: pygame.Color):
        self.x_position = x_position
        self.y_position = y_position + 80
        self.block_description = block_description
        self.background_color = background_color
        self.figure = None
        self.last_drawn_rects = []

        font = pygame.font.Font(
            "Font/OpenDyslexic3-Regular.ttf", 40)
        self.headline = TextView(
            font, self.color, x_position, y_position)
        self.headline.update_text("Next")

    def update_figure(self, figure: Figure):
        self.figure = deepcopy(figure)

    def draw(self, parent_surface: pygame.Surface) -> list[pygame.Rect]:
        if not self.figure:
            return []

        self.last_drawn_rects.clear()
        self.headline.draw(parent_surface)

        rect_width = 4 * self.block_description.width
        rect_height = 5 * self.block_description.width
        frame_rect = pygame.Rect(
            self.x_position, self.y_position, rect_width, rect_height)
        draw_frame(parent_surface, frame_rect, self.block_description)
        self.last_drawn_rects.append(frame_rect)

        offset = self.figure.get_static_offset()
        for block in self.figure.get_static_blocks():
            x_position = self.x_position + \
                (block.x + 1 + offset.x) * self.block_description.width
            y_position = self.y_position + \
                (block.y + 0.5 + offset.y) * self.block_description.height
            block_view = BlockView(
                x_position, y_position, self.block_description, self.figure.block_color)
            block_view.draw(parent_surface)

        return [frame_rect]
