from typing import List
from enum import Enum
from pygame import Color

from Common import *


class Position:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


FigureDescription = list[Position]


class BlockColor:
    body_color: Color
    border_color: Color

    def __init__(self,  body_color: Color, border_color: Color):
        self.body_color = body_color
        self.border_color = border_color


class Figure:
    position: Position
    relative_positions: list[Position]
    block_color: BlockColor

    def __init__(self, position: Position, figure_descriptions: List[FigureDescription], block_color: BlockColor):
        self.position = position
        self.figure_descriptions = figure_descriptions
        self.block_color = block_color

    def move(self, direction: Direction):
        match direction:
            case Direction.up:
                old_figure_description = self.figure_descriptions.pop(0)
                self.figure_descriptions.append(old_figure_description)
            case Direction.right:
                self.position.x += 1
            case Direction.left:
                self.position.x -= 1
            case Direction.down:
                self.position.y += 1

    def _get_blocks_internal(self, position: Position, figure_description: FigureDescription) -> list[Position]:
        blocks = [Position(position.x + rel_pos.x, position.y + rel_pos.y)
                  for rel_pos in figure_description]
        blocks.append(position)
        return blocks

    def get_blocks_for_next_move(self, direction: Direction) -> list[Position]:
        new_position_x = self.position.x
        new_position_y = self.position.y
        used_figure_description = self.figure_descriptions[0]
        match direction:
            case Direction.up:
                if len(self.figure_descriptions) > 1:
                    used_figure_description = self.figure_descriptions[1]
            case Direction.right:
                new_position_x += 1
            case Direction.left:
                new_position_x -= 1
            case Direction.down:
                new_position_y += 1

        return self._get_blocks_internal(Position(new_position_x, new_position_y), used_figure_description)

    def get_blocks(self) -> list[Position]:
        return self._get_blocks_internal(self.position, self.figure_descriptions[0])


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
                    Position(-2, 0), Position(-1, 0), Position(1, 0)]
                vertical_description = [
                    Position(0, -1), Position(0, 1), Position(0, 2)]
                block_color = BlockColor(Color_cyan, Color_cyan_dark)
                return Figure(position, [horizontal_description, vertical_description], block_color)

            case FigureBuilder.FigureType.O:
                description = [Position(1, 0), Position(1, 1), Position(0, 1)]
                block_description = BlockColor(Color_yellow, Color_yellow_dark)
                return Figure(position, [description], block_description)

            case FigureBuilder.FigureType.T:
                up_description = [
                    Position(-1, 0), Position(1, 0), Position(0, -1)]
                right_description = [
                    Position(0, -1), Position(0, 1), Position(1, 0)]
                down_description = [
                    Position(-1, 0), Position(1, 0), Position(0, 1)]
                left_description = [
                    Position(0, -1), Position(0, 1), Position(-1, 0)]
                block_color = BlockColor(Color_purple, Color_purple_dark)
                return Figure(position, [up_description, right_description, down_description, left_description], block_color)

            case FigureBuilder.FigureType.L:
                up_description = [
                    Position(0, 1), Position(0, 2), Position(1, 2)]
                right_description = [
                    Position(-1, 0), Position(1, 0), Position(1, -1)]
                down_description = [
                    Position(-1, 0), Position(0, 1), Position(0, 2)]
                left_description = [
                    Position(-1, 0), Position(-1, 1), Position(1, 0)]
                block_color = BlockColor(Color_orange, Color_orange_dark)
                return Figure(position, [up_description, right_description, down_description, left_description], block_color)

            case FigureBuilder.FigureType.J:
                up_description = [
                    Position(0, -1), Position(0, 1), Position(-1, 1)]
                right_description = [
                    Position(-1, 0), Position(1, 0), Position(1, 1)]
                down_description = [
                    Position(1, 0), Position(0, 1), Position(0, 2)]
                left_description = [
                    Position(-1, 0), Position(-1, -1), Position(1, 0)]
                block_color = BlockColor(Color_blue, Color_blue_dark)
                return Figure(position, [up_description, right_description, down_description, left_description], block_color)

            case FigureBuilder.FigureType.Z:
                horizontal_description = [
                    Position(-1, 0), Position(0, 1), Position(1, 1)]
                vertical_description = [
                    Position(0, 1), Position(1, 0), Position(1, -1)]
                block_color = BlockColor(Color_red, Color_red_dark)
                return Figure(position, [horizontal_description, vertical_description], block_color)

            case FigureBuilder.FigureType.S:
                horizontal_description = [
                    Position(0, 1), Position(-1, 1), Position(1, 0)]
                vertical_description = [
                    Position(0, -1), Position(1, 0), Position(1, 1)]
                block_color = BlockColor(Color_green, Color_green_dark)
                return Figure(position, [horizontal_description, vertical_description], block_color)
