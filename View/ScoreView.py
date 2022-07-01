

import pygame
from View.DrawSupport import draw_frame
from View.TextView import TextView
from View.ViewCommon import *


class ScoreView:
    text: str = "Score"
    score_x_padding: int = 10

    x_position: int
    y_position: int
    width: int
    height: int
    block_description: BlockDescription
    score_text: TextView
    score_value: TextView
    frame_rect: pygame.Rect

    def __init__(self, x_position: int, y_position: int, width: int, height: int,
                 block_description: BlockDescription):
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        self.block_description = block_description

        # Init score text
        self.score_text = TextView(
            medium_font, text_color, x_position, y_position)
        self.score_text.update_text(self.text)

        # Init frame
        frame_width = 4 * block_description.width
        frame_height = 2 * block_description.width
        frame_y_position = y_position + medium_font_height
        self.frame_rect = pygame.Rect(
            x_position, frame_y_position, frame_width, frame_height)

        # Init score value
        score_value_view_x_position = x_position + \
            frame_width / 2 - 1.5 * block_description.width + self.score_x_padding
        score_value_view_y_position = y_position + frame_height / 1.5
        self.score_value = TextView(
            big_font, text_color, score_value_view_x_position, score_value_view_y_position)

    def update(self, score: int, parent_surface: pygame.Surface):
        if self.score_value.update_text(str(score)):
            self.score_value.draw(parent_surface)

    def draw(self, parent_surface: pygame.Surface) -> list[pygame.Rect]:
        self.score_text.draw(parent_surface)
        draw_frame(parent_surface, self.frame_rect, self.block_description)
        self.score_value.draw(parent_surface)
        return [self.frame_rect]
