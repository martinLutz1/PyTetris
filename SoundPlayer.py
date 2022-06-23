
from enum import Enum
import pygame


class Sound(Enum):
    clear_row = 0
    clear_row_perfect = 1
    move_figure = 2
    landing = 3
    gameover = 4


class SoundPlayer:
    clear_row_sound: pygame.mixer.Sound
    clear_row_perfect_sound: pygame.mixer.Sound
    move_figure_sound: pygame.mixer.Sound
    landing_sound: pygame.mixer.Sound
    gameover_sound: pygame.mixer.Sound

    def __init__(self):
        volume = 0.1
        pygame.mixer.pre_init()
        pygame.mixer.init()

        pygame.mixer.music.load("Music/Tetris_theme.ogg")
        pygame.mixer.music.set_volume(volume)
        self.clear_row_sound = pygame.mixer.Sound("Music/clear_row.wav")
        self.clear_row_sound.set_volume(volume)
        self.clear_row_perfect_sound = pygame.mixer.Sound(
            "Music/clear_row_perfect.wav")
        self.clear_row_perfect_sound.set_volume(volume)
        self.move_figure_sound = pygame.mixer.Sound("Music/move_figure.wav")
        self.move_figure_sound.set_volume(volume / 4)

        self.landing_sound = pygame.mixer.Sound("Music/landing.wav")
        self.landing_sound.set_volume(volume / 2)

        self.gameover_sound = pygame.mixer.Sound("Music/gameover.wav")
        self.gameover_sound.set_volume(volume)

    def play_theme(self):
        pygame.mixer.music.play(-1)

    def stop_theme(self):
        pygame.mixer.music.pause()

    def _to_pygame_sound(self, sound: Sound) -> pygame.mixer.Sound:
        match sound:
            case Sound.clear_row: return self.clear_row_sound
            case Sound.clear_row_perfect: return self.clear_row_perfect_sound
            case Sound.move_figure: return self.move_figure_sound
            case Sound.landing: return self.landing_sound
            case Sound.gameover: return self.gameover_sound

    def play_sound(self, sound: Sound):
        pygame_sound = self._to_pygame_sound(sound)
        pygame.mixer.Sound.play(pygame_sound)
