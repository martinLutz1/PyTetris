

import pygame
from View.DrawSupport import draw_frame
from View.TextView import TextView
from View.ViewCommon import BlockDescription


class ScoreView:
    color: pygame.Color = (30, 30, 30)
    width: int
    height: int
    x_position: int
    y_position: int
    block_description: BlockDescription

    score_text: TextView
    score_value: TextView

    def __init__(self, x_position: int, y_position: int, width: int, height: int,
                 block_description: BlockDescription):
        self.width = width
        self.height = height
        self.x_position = x_position
        self.y_position = y_position + 80
        self.block_description = block_description
        score_text_font = pygame.font.Font(
            "Font/OpenDyslexic3-Regular.ttf", 40)
        self.score_text = TextView(
            score_text_font, self.color, x_position, y_position)
        self.score_text.update_text("Score")

        rect_width = 4 * self.block_description.width  # Max block widht: 2
        rect_height = 2 * self.block_description.width  # Max block height: 4

        score_value_font = pygame.font.Font(
            "Font/OpenDyslexic3-Regular.ttf", 50)
        score_value_view_x_position = x_position + \
            rect_width / 2 - 1.5 * block_description.width
        score_value_view_y_position = y_position + rect_height / 2 + 20

        self.score_value = TextView(
            score_value_font, self.color, score_value_view_x_position, score_value_view_y_position)

    def update(self, score: int, parent_surface: pygame.Surface):
        if self.score_value.update_text(str(score)):
            self.score_text.draw(parent_surface)
            self.score_value.draw(parent_surface)

    def draw(self, parent_surface: pygame.Surface) -> list[pygame.Rect]:
        self.score_text.draw(parent_surface)

        rect_width = 4 * self.block_description.width  # Max block widht: 2
        rect_height = 2 * self.block_description.width  # Max block height: 4
        border_rect = pygame.Rect(
            self.x_position, self.y_position, rect_width, rect_height)
        draw_frame(parent_surface, border_rect, self.block_description)

        self.score_value.draw(parent_surface)
        return [border_rect]
