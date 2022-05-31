import pygame
from Common import Direction


class KeyPressHandler:
    is_direction_key_pressed = [False, False, False, False]
    is_quit_pressed = False

    def _to_index(self, key_constant: int):
        if (key_constant == pygame.K_RIGHT) or (key_constant == pygame.K_d):
            return Direction.right.value
        elif (key_constant == pygame.K_LEFT) or (key_constant == pygame.K_a):
            return Direction.left.value
        elif (key_constant == pygame.K_DOWN) or (key_constant == pygame.K_s):
            return Direction.down.value
        elif (key_constant == pygame.K_UP) or (key_constant == pygame.K_w):
            return Direction.up.value
        else:
            return -1

    def update_pressed_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_quit_pressed = True
            if event.type == pygame.KEYDOWN:
                direction_key_index = self._to_index(event.key)
                if direction_key_index != -1:
                    self.is_direction_key_pressed[direction_key_index] = True
                elif event.key == pygame.K_ESCAPE:
                    self.is_quit_pressed = True
            elif event.type == pygame.KEYUP:
                direction_key_index = self._to_index(event.key)
                if direction_key_index != -1:
                    self.is_direction_key_pressed[direction_key_index] = False
