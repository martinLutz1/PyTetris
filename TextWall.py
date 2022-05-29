# Original from https://stackoverflow.com/questions/15488293/render-anti-aliased-text-on-transparent-surface-in-pygame
import pygame
from pygame import Surface
from pygame.locals import *

from Figures import Position


class TextWall():
    use_antialiasing: bool = True

    font: pygame.font.Font
    color: pygame.Color
    position: Position
    text_message: str
    screen: pygame.Surface
    text_surface: pygame.Surface
    text_rect: pygame.Rect

    def __init__(self, font: pygame.font.Font, color: pygame.Color,
                 position: Position, surface: pygame.Surface):
        self.font = font
        self.color = color
        self.text_message = ""
        self.screen = surface
        self.position = position

    def _render(self):
        """no AA = automatic transparent. With AA you need to set the color key too"""
        self.text_surface = self.font.render(
            self.text_message, self.use_antialiasing, self.color)
        self.text_rect = self.text_surface.get_rect(
            center=(self.position.x, self.position.y))

    def draw(self):
        self._render()
        self.screen.blit(self.text_surface, self.text_rect)

    def update_text(self, text):
        if text is not self.text_message:
            self.text_message = text
            self.draw()
