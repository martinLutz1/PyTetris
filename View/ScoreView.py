# Original from https://stackoverflow.com/questions/15488293/render-anti-aliased-text-on-transparent-surface-in-pygame
import pygame

from Figures import BlockPosition


class TextView():
    use_antialiasing: bool = True

    font: pygame.font.Font
    color: pygame.Color
    position: BlockPosition
    text: str
    surface: pygame.Surface
    rect: pygame.Rect

    def __init__(self, font: pygame.font.Font, color: pygame.Color,
                 position: BlockPosition):
        self.font = font
        self.color = color
        self.text = ""
        self.position = position

    def _render(self):
        """no AA = automatic transparent. With AA you need to set the color key too"""
        self.surface = self.font.render(
            self.text, self.use_antialiasing, self.color)
        self.rect = self.surface.get_rect(
            center=(self.position.x, self.position.y))

    def draw(self, parent_surface: pygame.Surface):
        self._render()
        parent_surface.blit(self.surface, self.rect)

    # Returns whether the text was updated.
    def update_text(self, text: str) -> bool:
        if self.text != text:
            self.text = text
            return True
        else:
            return False


class ScoreView:
    color: pygame.Color = (40, 40, 40)
    max_screen_distance: int = 10

    font: pygame.font.Font
    text_wall: TextView

    def __init__(self, screen_width: int, screen_height: int):
        self.font = pygame.font.Font("Font/OpenDyslexic3-Regular.ttf", 50)

        def get_score_position():
            y_score_position_candidate = int(screen_height * 0.05)
            y_score_position = self.max_screen_distance if (
                y_score_position_candidate > ScoreView.max_screen_distance) else y_score_position_candidate

            x_score_position_candidate = int(screen_width * 0.95)
            x_score_position = screen_width - self.max_screen_distance if (
                (screen_width - x_score_position_candidate) > ScoreView.max_screen_distance) else x_score_position_candidate
            score_width, score_height = self.font.size(self._get_score_text(0))

            return BlockPosition(x_score_position - score_width, y_score_position + score_height)

        self.text_wall = TextView(
            self.font, self.color, get_score_position())

    def _get_score_text(self, score: int):
        return "Score: " + str(score)

    def update(self, score: int, parent_surface: pygame.Surface):
        if self.text_wall.update_text(self._get_score_text(score)):
            self.text_wall.draw(parent_surface)

    def draw(self, parent_surface: pygame.Surface):
        self.text_wall.draw(parent_surface)
