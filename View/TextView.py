import pygame


class TextView():
    # Original from https://stackoverflow.com/questions/15488293/render-anti-aliased-text-on-transparent-surface-in-pygame
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
        self.x_position = x_position
        self.y_position = y_position

    def _render(self):
        """no AA = automatic transparent. With AA you need to set the color key too"""
        self.surface = self.font.render(
            self.text, self.use_antialiasing, self.color)
        self.rect = self.surface.get_rect(
            center=(self.x_position, self.y_position))
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
