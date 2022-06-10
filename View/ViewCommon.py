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
