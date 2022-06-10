from copy import deepcopy
import pygame

from Figures import BlockColor, BlockPosition, Offset
from View.DrawSupport import draw_bordered_rounded_rect
from View.ViewCommon import BlockDescription


class BlockView:
    position: BlockPosition
    offset: Offset
    color: BlockColor

    def __init__(self, block_description: BlockDescription, position: BlockPosition,
                 offset: Offset, color: BlockColor):
        self.block_description = block_description
        self.position = position
        self.offset = offset
        self.color = color

    def update_position(self, position: BlockPosition, offset: Offset):
        self.position = deepcopy(position)
        self.offset = deepcopy(offset)

    def draw(self, parent_surface: pygame.Surface) -> pygame.Rect:
        x_position = (float(self.position.x) + self.offset.x) * \
            self.block_description.width
        y_position = (float(self.position.y) + self.offset.y) * \
            self.block_description.height
        block_rect = pygame.Rect(
            x_position, y_position, self.block_description.width, self.block_description.height)
        draw_bordered_rounded_rect(parent_surface, deepcopy(block_rect), self.color.body_color,
                                   self.color.border_color, 10, self.block_description.border_thickness)
        return block_rect
