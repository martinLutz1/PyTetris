import pygame

from View.ScoreView import ScoreView


class TetrisInfoView:
    surface: pygame.Surface
    score_view: ScoreView
    x_position: int
    y_position: int

    background_color: pygame.Color = (50, 50, 50)

    def __init__(self, width: int, height: int, x_position: int, y_position: int):
        self.surface = pygame.Surface((width, height))
        self.x_position = x_position
        self.y_position = y_position

        self.score_view = ScoreView(x_position, y_position, width, height)

    def update_score(self, score: int):
        self.score_view.update(score, self.surface)

    def draw(self, parent_surface: pygame.Surface):
        self.score_view.draw(parent_surface)
