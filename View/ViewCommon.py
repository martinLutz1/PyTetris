import pygame

# Make sure pygame is initialized to be able to instantiate fonts.
pygame.init()


class BlockDescription:
    height: int
    width: int
    border_thickness: int

    def __init__(self, width: int, height: int, border_thickness: int):
        self.width = width
        self.height = height
        self.border_thickness = border_thickness


class ViewDescription:
    screen_width: int
    screen_height: int
    tetris_width: int
    tetris_area_x_offset: int

    def __init__(self, screen_width: int, screen_height: int, tetris_width: int, x_screen_offset: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tetris_width = tetris_width
        self.tetris_area_x_offset: int = x_screen_offset


_font_path: str = "Font/OpenDyslexic3-Regular.ttf"

medium_font = pygame.font.Font(_font_path, 40)
medium_font_height: int = 80

big_font = pygame.font.Font(_font_path, 50)
big_font_height: int = 120
text_color = pygame.Color(30, 30, 30)
