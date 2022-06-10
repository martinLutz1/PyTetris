from copy import deepcopy
import pygame

from Figures import BlockColor, BlockPosition, Figure, Offset
from View.DrawSupport import draw_bordered_rounded_rect
from View.ViewCommon import BlockDescription


class BlockSprite(pygame.sprite.Sprite):
    number_of_offscreen_rows: int

    def __init__(self, description: BlockDescription, position: BlockPosition,
                 offset: Offset, color: BlockColor, background_color: pygame.Color,
                 number_of_offscreen_rows: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(
            (description.width, description.height))
        self.rect = self.image.get_rect()
        self.image.fill(background_color, self.rect)
        draw_bordered_rounded_rect(self.image, deepcopy(self.rect), color.body_color,
                                   color.border_color, 10, description.border_thickness)
        self.number_of_offscreen_rows = number_of_offscreen_rows
        self.update(position, offset)

    def update(self, block_position: BlockPosition, offset: Offset):
        x_position = (float(block_position.x) + offset.x) * self.rect.width
        y_position = (float(block_position.y - self.number_of_offscreen_rows) + offset.y) * \
            self.rect.height
        self.rect.x = x_position
        self.rect.y = y_position


class FigureSprite():
    block_sprite_group: pygame.sprite.RenderUpdates
    position: BlockPosition
    background_color: pygame.Color
    last_drawn_rects: list[pygame.Rect]

    def __init__(self, figure: Figure, block_description: BlockDescription,
                 number_of_offscreen_rows: int, background_color: pygame.Color):
        block_sprites = []
        for block_position in figure.get_blocks():
            block_sprite = BlockSprite(
                block_description, block_position, figure.offset,
                figure.block_color, background_color, number_of_offscreen_rows)
            block_sprites.append(block_sprite)

        self.block_sprite_group = pygame.sprite.RenderUpdates(block_sprites)
        self.update_position(figure)
        self.background_color = background_color
        self.last_drawn_rects = []

    def update_position(self, figure: Figure):
        self.position = deepcopy(figure.position)

        blocks = figure.get_blocks()
        sprites = self.block_sprite_group.sprites()
        if len(blocks) != len(sprites):
            raise Exception(
                "The number of blocks in the passed figure does not match the number of sprites.")
        for i in range(len(sprites)):
            sprites[i].update(blocks[i], figure.offset)

    def draw(self, parent_surface: pygame.Surface) -> list[pygame.Rect]:
        if self.position.y >= -1:
            updated_rects = self.block_sprite_group.draw(parent_surface)
            self.last_drawn_rects = deepcopy(updated_rects)
            return updated_rects

        return []

    def clear(self, parent_surface: pygame.Surface) -> list[pygame.Rect]:
        for rect in self.last_drawn_rects:
            parent_surface.fill(self.background_color, rect)
        return self.last_drawn_rects
