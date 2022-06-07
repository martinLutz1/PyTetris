from copy import deepcopy
from typing import List
from enum import Enum
from pygame import Color

from Common import *


class Offset:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class BlockPosition:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


FigureDescription = list[BlockPosition]


class BlockColor:
    body_color: Color
    border_color: Color

    def __init__(self,  body_color: Color, border_color: Color):
        self.body_color = body_color
        self.border_color = border_color


class MovementDescription:
    direction: Direction
    duration_ms: int

    def __init__(self, direction: Direction, duration_ms: int):
        self.direction = direction
        self.duration_ms = duration_ms


class Figure:
    position: BlockPosition
    relative_positions: list[BlockPosition]
    offset: Offset
    block_color: BlockColor
    ms_elapsed_since_last_step: int

    horizontal_movement_converter: DurationToFactorConverter = None
    vertical_movement_converter: DurationToFactorConverter = None
    next_vertical_move: MovementDescription = None
    next_horizontal_move: MovementDescription = None

    def __init__(self, position: BlockPosition, figure_descriptions: List[FigureDescription], block_color: BlockColor):
        self.position = position
        self.figure_descriptions = figure_descriptions
        self.block_color = block_color
        self.offset = Offset(0.0, 0.0)

    def update_position(self):
        if self.vertical_movement_converter:
            partial_block_offset_factor = self.vertical_movement_converter.get_factor()
            if partial_block_offset_factor >= 1:
                self.position.y += 1
                self.offset.y = 0.0
                self.vertical_movement_converter = None
            else:
                if self.offset.y < partial_block_offset_factor:
                    self.offset.y = partial_block_offset_factor

        if self.horizontal_movement_converter:
            partial_block_offset_factor = self.horizontal_movement_converter.get_factor()
            if partial_block_offset_factor >= 1:
                self.position.x += 1
                self.offset.x = 0.0
                self.horizontal_movement_converter = None
            elif partial_block_offset_factor <= -1:
                self.position.x -= 1
                self.offset.x = 0.0
                self.horizontal_movement_converter = None
            else:
                self.offset.x = partial_block_offset_factor

    def moves_down(self):
        return self.vertical_movement_converter is not None

    # Move the figure to the passed direction. The movement lasts for the passed duration.
    def move(self, direction: Direction, duration_ms: int):
        # Rotate
        if direction == Direction.up:
            old_figure_description = self.figure_descriptions.pop(0)
            self.figure_descriptions.append(old_figure_description)

        # Vertical (down) movement
        if direction == Direction.down:
            if not self.vertical_movement_converter:
                self.vertical_movement_converter = DurationToFactorConverter(
                    duration_ms)
            elif self.vertical_movement_converter.duration_ms > duration_ms:
                self.vertical_movement_converter = DurationToFactorConverter(
                    duration_ms, False, self.vertical_movement_converter.get_factor())

        # Horizontal movement
        if not self.horizontal_movement_converter:
            if direction == Direction.left:
                self.horizontal_movement_converter = DurationToFactorConverter(
                    duration_ms, True)
            elif direction == Direction.right:
                self.horizontal_movement_converter = DurationToFactorConverter(
                    duration_ms, False)

    def _get_blocks_internal(self, position: BlockPosition, figure_description: FigureDescription) -> list[BlockPosition]:
        blocks = [BlockPosition(position.x + rel_pos.x, position.y + rel_pos.y)
                  for rel_pos in figure_description]
        blocks.append(position)
        return blocks

    def get_blocks_for_next_move(self, direction: Direction) -> list[BlockPosition]:
        next_move_block_position = deepcopy(self.position)
        used_figure_description = self.figure_descriptions[0]

        match direction:
            case Direction.up:
                if len(self.figure_descriptions) > 1:
                    used_figure_description = self.figure_descriptions[1]
            case Direction.right:
                next_move_block_position.x += 1
            case Direction.left:
                next_move_block_position.x -= 1
            case Direction.down:
                next_move_block_position.y += 1

        return self._get_blocks_internal(next_move_block_position, used_figure_description)

    def get_blocks(self) -> list[BlockPosition]:
        return self._get_blocks_internal(self.position, self.figure_descriptions[0])

    # Stop any ongoing movement and snap to the target position.
    def finalize(self, x_border: int, y_border: int):
        if self.vertical_movement_converter:
            self.position.y += -1 if self.vertical_movement_converter.is_negative else 1
            self.vertical_movement_converter = None
        self.offset.y = 0.0

        if self.horizontal_movement_converter:
            self.position.x += -1 if self.horizontal_movement_converter.is_negative else 1
            self.horizontal_movement_converter = None
        self.offset.x = 0.0


class FigureBuilder:
    class FigureType(Enum):
        I = 0
        O = 1
        T = 2
        S = 3
        Z = 4
        J = 5
        L = 6

    def new(position, figure_type: FigureType) -> Figure:
        match figure_type:
            case FigureBuilder.FigureType.I:
                horizontal_description = [
                    BlockPosition(-2, 0), BlockPosition(-1, 0), BlockPosition(1, 0)]
                vertical_description = [
                    BlockPosition(0, -1), BlockPosition(0, 1), BlockPosition(0, 2)]
                block_color = BlockColor(Color_cyan, Color_cyan_dark)
                return Figure(position, [horizontal_description, vertical_description], block_color)

            case FigureBuilder.FigureType.O:
                description = [BlockPosition(1, 0), BlockPosition(
                    1, 1), BlockPosition(0, 1)]
                block_description = BlockColor(Color_yellow, Color_yellow_dark)
                return Figure(position, [description], block_description)

            case FigureBuilder.FigureType.T:
                up_description = [
                    BlockPosition(-1, 0), BlockPosition(1, 0), BlockPosition(0, -1)]
                right_description = [
                    BlockPosition(0, -1), BlockPosition(0, 1), BlockPosition(1, 0)]
                down_description = [
                    BlockPosition(-1, 0), BlockPosition(1, 0), BlockPosition(0, 1)]
                left_description = [
                    BlockPosition(0, -1), BlockPosition(0, 1), BlockPosition(-1, 0)]
                block_color = BlockColor(Color_purple, Color_purple_dark)
                return Figure(position, [up_description, right_description, down_description, left_description], block_color)

            case FigureBuilder.FigureType.L:
                up_description = [
                    BlockPosition(-1, 0), BlockPosition(1, 0), BlockPosition(1, -1)]
                right_description = [
                    BlockPosition(-1, 0), BlockPosition(0, 1), BlockPosition(0, 2)]
                down_description = [
                    BlockPosition(-1, 0), BlockPosition(-1, 1), BlockPosition(1, 0)]
                left_description = [
                    BlockPosition(0, 1), BlockPosition(0, 2), BlockPosition(1, 2)]

                block_color = BlockColor(Color_orange, Color_orange_dark)
                return Figure(position, [up_description, right_description, down_description, left_description], block_color)

            case FigureBuilder.FigureType.J:
                up_description = [
                    BlockPosition(0, -1), BlockPosition(0, 1), BlockPosition(-1, 1)]
                right_description = [
                    BlockPosition(-1, 0), BlockPosition(1, 0), BlockPosition(1, 1)]
                down_description = [
                    BlockPosition(1, 0), BlockPosition(0, 1), BlockPosition(0, 2)]
                left_description = [
                    BlockPosition(-1, 0), BlockPosition(-1, -1), BlockPosition(1, 0)]
                block_color = BlockColor(Color_blue, Color_blue_dark)
                return Figure(position, [up_description, right_description, down_description, left_description], block_color)

            case FigureBuilder.FigureType.Z:
                horizontal_description = [
                    BlockPosition(-1, 0), BlockPosition(0, 1), BlockPosition(1, 1)]
                vertical_description = [
                    BlockPosition(0, 1), BlockPosition(1, 0), BlockPosition(1, -1)]
                block_color = BlockColor(Color_red, Color_red_dark)
                return Figure(position, [horizontal_description, vertical_description], block_color)

            case FigureBuilder.FigureType.S:
                horizontal_description = [
                    BlockPosition(0, 1), BlockPosition(-1, 1), BlockPosition(1, 0)]
                vertical_description = [
                    BlockPosition(0, -1), BlockPosition(1, 0), BlockPosition(1, 1)]
                block_color = BlockColor(Color_green, Color_green_dark)
                return Figure(position, [horizontal_description, vertical_description], block_color)
