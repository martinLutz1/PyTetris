from enum import Enum
from pygame import Color
import time

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


class DurationToFactorConverter:
    ms_elapsed_on_start: int
    duration_ms: int
    is_negative: bool
    factor_offset: float

    def __init__(self, duration_ms: int, is_negative: bool = False, factor_offset: float = 0.0) -> None:
        self.duration_ms = duration_ms
        self.ms_elapsed_on_start = time.time() * 1000
        self.is_negative = is_negative
        self.factor_offset = factor_offset

    def reset(self):
        self.ms_elapsed_on_start = time.time() * 1000

    def get_factor(self) -> float:
        ms_elapsed_now = time.time() * 1000
        ms_elapsed_since_start = ms_elapsed_now - self.ms_elapsed_on_start

        factor = min((ms_elapsed_since_start /
                     self.duration_ms) + self.factor_offset, 1.0)
        if self.is_negative:
            return -1.0 * factor
        else:
            return factor
