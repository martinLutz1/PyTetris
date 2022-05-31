from enum import Enum
from pygame import Color

Color_cyan = Color(0, 240, 240)
Color_cyan_dark = Color(0, 50, 50)
Color_yellow = Color(255, 255, 0)
Color_yellow_dark = Color(40, 40, 0)
Color_purple = Color(160, 0, 240)
Color_purple_dark = Color(40, 0, 50)
Color_orange = Color(240, 160, 0)
Color_orange_dark = Color(50, 40, 0)
Color_blue = Color(0, 0, 240)
Color_blue_dark = Color(0, 0, 50)
Color_red = Color(240, 0, 0)
Color_red_dark = Color(50, 0, 0)
Color_green = Color(0, 240, 0)
Color_green_dark = Color(0, 50, 0)


class Direction(Enum):
    up = 0
    down = 1
    left = 2
    right = 3
