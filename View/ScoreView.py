# Original from https://stackoverflow.com/questions/15488293/render-anti-aliased-text-on-transparent-surface-in-pygame
import pygame


class TextView():
    use_antialiasing: bool = True

    font: pygame.font.Font
    color: pygame.Color
    text: str
    surface: pygame.Surface
    rect: pygame.Rect
    x_position: int
    y_position: int

    def __init__(self, font: pygame.font.Font, color: pygame.Color, x_position: int, y_position: int):
        self.font = font
        self.color = color
        self.text = ""
        self.x_position = x_position + 100
        self.y_position = y_position + 20

    def _render(self):
        """no AA = automatic transparent. With AA you need to set the color key too"""
        self.surface = self.font.render(
            self.text, self.use_antialiasing, self.color)
        self.rect = self.surface.get_rect()
        self.rect.x = self.x_position
        self.rect.y = self.y_position

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
    width: int
    height: int

    font: pygame.font.Font
    text_wall: TextView

    def __init__(self, x_position: int, y_position: int, width: int, height: int):
        self.font = pygame.font.Font("Font/OpenDyslexic3-Regular.ttf", 50)
        self.width = width
        self.height = height
        text_y_position = y_position + height / 2 - self.font.get_height()
        self.text_wall = TextView(
            self.font, self.color, x_position, text_y_position)

    def _get_score_text(self, score: int):
        return "Score: " + str(score)

    def update(self, score: int, parent_surface: pygame.Surface):
        if self.text_wall.update_text(self._get_score_text(score)):
            self.text_wall.draw(parent_surface)

    def draw(self, parent_surface: pygame.Surface):
        self.text_wall.draw(parent_surface)
