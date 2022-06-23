from copy import deepcopy
import pygame
from Figures import Figure
from View.FigurePreviewView import FigurePreviewView

from View.ScoreView import ScoreView
from View.ViewCommon import BlockDescription


class TetrisInfoView:
    surface: pygame.Surface
    score_view: ScoreView
    figure_preview_view: FigurePreviewView

    x_position: int
    y_position: int

    def __init__(self, width: int, height: int, x_position: int, y_position: int,
                 block_description: BlockDescription, background_color: pygame.Color):
        self.surface = pygame.Surface((width, height))
        self.x_position = x_position
        self.y_position = y_position

        sub_area_height = 250
        current_y_position = y_position
        padding = 80
        self.score_view = ScoreView(
            x_position + padding, current_y_position, width, sub_area_height, block_description)

        current_y_position += sub_area_height
        self.figure_preview_view = FigurePreviewView(
            x_position + padding, current_y_position, block_description, background_color)

    def update_score(self, score: int):
        self.score_view.update(score, self.surface)

    def update_figure_preview(self, figure: Figure):
        self.figure_preview_view.update_figure(figure)

    def draw_score(self, parent_surface: pygame.Surface):
        self.score_view.draw(parent_surface)

    def draw_figure_preview(self, parent_surface: pygame.Surface) -> list[pygame.Rect]:
        updated_rects = self.figure_preview_view.draw(parent_surface)
        return updated_rects
