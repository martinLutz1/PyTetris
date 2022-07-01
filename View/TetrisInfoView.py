from Figures import Figure
from View.FigurePreviewView import FigurePreviewView
from View.ScoreView import ScoreView
from View.ViewCommon import BlockDescription

import pygame


class TetrisInfoView:
    x_padding: int = 80
    sub_area_height: int = 240

    surface: pygame.Surface
    score_view: ScoreView
    figure_preview_view: FigurePreviewView

    x_position: int
    y_position: int

    def __init__(self, x_position: int, y_position: int, width: int, height: int,  block_description: BlockDescription):
        self.surface = pygame.Surface((width, height))
        self.x_position = x_position
        self.y_position = y_position

        # Init score view
        current_y_position = y_position
        self.score_view = ScoreView(
            x_position + self.x_padding, current_y_position, width, self.sub_area_height, block_description)

        # Init figure preview view
        current_y_position += self.sub_area_height
        self.figure_preview_view = FigurePreviewView(
            x_position + self.x_padding, current_y_position, block_description)

    def update_score(self, score: int):
        self.score_view.update(score, self.surface)

    def update_figure_preview(self, figure: Figure):
        self.figure_preview_view.update_figure(figure)

    def draw_score(self, parent_surface: pygame.Surface):
        self.score_view.draw(parent_surface)

    def draw_figure_preview(self, parent_surface: pygame.Surface) -> list[pygame.Rect]:
        updated_rects = self.figure_preview_view.draw(parent_surface)
        return updated_rects
