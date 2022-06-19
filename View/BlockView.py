from copy import deepcopy
from turtle import color
import pygame

from Figures import BlockColor, BlockPosition, Offset
from View.DrawSupport import draw_bordered_rounded_rect
from View.ViewCommon import BlockDescription


class BlockView:
    x_position: float
    y_position: float
    block_description: BlockDescription
    color: BlockColor

    def __init__(self, x_position: int, y_position: int,
                 block_description: BlockDescription, color: pygame.Color):
        self.x_position = x_position
        self.y_position = y_position
        self.block_description = block_description
        self.color = color

    def draw(self, parent_surface: pygame.Surface) -> pygame.Rect:
        block_rect = pygame.Rect(
            self.x_position, self.y_position, self.block_description.width, self.block_description.height)
        draw_bordered_rounded_rect(parent_surface, deepcopy(block_rect), self.color.body_color,
                                   self.color.border_color, 10, self.block_description.border_thickness)
        return block_rect


class TetrisBlockView(BlockView):
    block_description: BlockDescription
    position: BlockPosition
    offset: Offset
    color: BlockColor

    def __init__(self, block_description: BlockDescription, position: BlockPosition,
                 offset: Offset, color: BlockColor):
        super().__init__(0, 0, block_description, color)
        self.block_description = block_description
        self.position = position
        self.offset = offset
        self.color = color

    def update_position(self, position: BlockPosition, offset: Offset):
        self.position = deepcopy(position)
        self.offset = deepcopy(offset)

    def draw(self, parent_surface: pygame.Surface) -> pygame.Rect:
        self.x_position = (float(self.position.x) + self.offset.x) * \
            self.block_description.width
        self.y_position = (float(self.position.y) + self.offset.y) * \
            self.block_description.height
        return super().draw(parent_surface)
