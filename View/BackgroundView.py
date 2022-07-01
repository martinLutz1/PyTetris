from View.ViewCommon import ViewDescription

import pygame


class BackgroundView:
    color: pygame.Color = (50, 50, 50)
    unused_area_color:  pygame.Color = (150, 150, 150)
    border_color: pygame.Color = (40, 40, 40)
    border_thickness: int = 20
    view_description: ViewDescription
    surface: pygame.Surface

    def __init__(self, width: int, height: int, view_description: ViewDescription):
        self.surface = pygame.Surface((width, height))
        self.view_description = view_description

    def _draw_border(self, x_position: int):
        border_rect = pygame.Rect(
            x_position, 0, self.border_thickness, self.view_description.screen_height)
        pygame.draw.rect(self.surface, self.border_color, border_rect)

    def _draw_unused_area(self, x_position: int):
        rect_width = self.view_description.tetris_area_x_offset - self.border_thickness
        border_rect = pygame.Rect(
            x_position, 0, rect_width, self.view_description.screen_height)
        pygame.draw.rect(self.surface, self.unused_area_color, border_rect)

    def draw(self, parent_surface: pygame.Surface):
        # Background color
        self.surface.fill(self.color)
        # Left area
        self._draw_border(
            self.view_description.tetris_area_x_offset - self.border_thickness)
        self._draw_unused_area(0)
        # Right area
        self._draw_border(self.view_description.screen_width -
                          self.view_description.tetris_area_x_offset)
        self._draw_unused_area(self.view_description.screen_width -
                               self.view_description.tetris_area_x_offset + self.border_thickness)

        parent_surface.blit(self.surface, (0, 0))
