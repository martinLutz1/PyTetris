from copy import deepcopy
import numpy
import pygame
from typing import List
from Figures import BlockColor, Figure

from View.BackgroundView import BackgroundView
from View.DrawSupport import *
from View.ScoreView import ScoreView
from View.TetrisInfoView import TetrisInfoView
from View.TetrisView import TetrisView
from View.ViewCommon import ViewDescription


class TetrisPainter:
    screen: pygame.Surface
    view_description: ViewDescription
    background_view: BackgroundView
    score_view: ScoreView
    tetris_view: TetrisView
    tetris_info_view: TetrisInfoView
    last_figure: Figure = None

    def __init__(self, number_of_rows: int, number_of_columns: int, number_of_offscreen_rows: int):
        screen_width = pygame.display.Info().current_w
        screen_height = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height), pygame.FULLSCREEN)

        tetris_view_width = screen_height / 2
        tetris_view_x_offset = (screen_width - tetris_view_width) / 2
        self.view_description = ViewDescription(
            screen_width, screen_height, tetris_view_width, tetris_view_x_offset)

        self.background_view = BackgroundView(
            screen_width, screen_height, self.view_description)

        self.tetris_view = TetrisView(
            tetris_view_width, screen_height, tetris_view_x_offset, 0,
            number_of_rows, number_of_columns, number_of_offscreen_rows)

        tetris_info_view_x_offset = tetris_view_x_offset + tetris_view_width
        self.tetris_info_view = TetrisInfoView(
            tetris_view_x_offset, screen_height, tetris_info_view_x_offset, 0)

        self.background_view.draw(self.screen)

    def draw_figure(self, figure: Figure, is_new_figure: bool):
        updated_rects = []

        if is_new_figure:
            if self.last_figure:
                self.tetris_view.add_to_static_blocks(self.last_figure)

            self.tetris_view.set_moving_figure(figure)
            self.last_figure = deepcopy(figure)
        else:
            cleared_rects = self.tetris_view.clear_moving_figure()
            updated_rects.extend(cleared_rects)
            self.tetris_view.update_figure_position(figure)

        figure_rects = self.tetris_view.draw_moving_figure()
        updated_rects.extend(figure_rects)

        self.tetris_view.blit(self.screen)
        pygame.display.update(updated_rects)

    def draw_score(self, score: int):
        self.tetris_info_view.update_score(score)
        self.tetris_info_view.draw(self.screen)

    def color_rows(self, rows: list[int], block_color: BlockColor):
        updated_rects = self.tetris_view.color_rows(
            rows, block_color, self.screen)
        pygame.display.update(updated_rects)

    def redraw_all(self, field: numpy.ndarray):
        self.background_view.draw(self.screen)
        self.tetris_info_view.draw(self.screen)
        self.tetris_view.set_static_blocks(field)
        self.tetris_view.draw_all(self.screen)
        pygame.display.update()
