from typing import List
from enum import Enum

from pygame import Color
from Common import Direction


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
            case Direction.UP:
                old_figure_description = self.figure_descriptions.pop(0)
                self.figure_descriptions.append(old_figure_description)
            case Direction.RIGHT:
                self.position.x += 1
            case Direction.LEFT:
                self.position.x -= 1
            case Direction.DOWN:
                self.position.y += 1

    def _get_used_points_internal(self, position: Position, figure_description: FigureDescription) -> list[Position]:
        used_points = [position]
        for relative_position in figure_description:
            absolute_x = used_points[0].x + relative_position.x
            absolute_y = used_points[0].y + relative_position.y
            used_points.append(Position(absolute_x, absolute_y))
        return used_points

    def get_next_move_used_points(self, direction: Direction) -> list[Position]:
        new_position_x = self.position.x
        new_position_y = self.position.y
        used_figure_description = self.figure_descriptions[0]
        match direction:
            case Direction.UP:
                if len(self.figure_descriptions) > 1:
                    used_figure_description = self.figure_descriptions[1]
            case Direction.RIGHT:
                new_position_x += 1
            case Direction.LEFT:
                new_position_x -= 1
            case Direction.DOWN:
                new_position_y += 1

        return self._get_used_points_internal(Position(new_position_x, new_position_y), used_figure_description)

    def get_used_points(self) -> list[Position]:
        return self._get_used_points_internal(self.position, self.figure_descriptions[0])


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
                block_color = BlockColor(
                    Color(0, 240, 240), Color(0, 40, 40))
                return Figure(position, [horizontal_description, vertical_description], block_color)

            case FigureBuilder.FigureType.O:
                description = [Position(1, 0), Position(1, 1), Position(0, 1)]
                block_description = BlockColor(
                    Color(0, 240, 240), Color(40, 40, 0))
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
                block_color = BlockColor(
                    Color(160, 0, 240), Color(30, 0, 45))
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
                block_color = BlockColor(
                    Color(240, 160, 0), Color(45, 30, 0))
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
                block_color = BlockColor(
                    Color(0, 0, 240), Color(0, 0, 40))
                return Figure(position, [up_description, right_description, down_description, left_description], block_color)

            case FigureBuilder.FigureType.Z:
                horizontal_description = [
                    Position(-1, 0), Position(0, 1), Position(1, 1)]
                vertical_description = [
                    Position(0, 1), Position(1, 0), Position(1, -1)]
                block_color = BlockColor(
                    Color(240, 0, 0), Color(40, 0, 0))
                return Figure(position, [horizontal_description, vertical_description], block_color)

            case FigureBuilder.FigureType.S:
                horizontal_description = [
                    Position(0, 1), Position(-1, 1), Position(1, 0)]
                vertical_description = [
                    Position(0, -1), Position(1, 0), Position(1, 1)]
                block_color = BlockColor(
                    Color(0, 240, 0), Color(0, 40, 0))
                return Figure(position, [horizontal_description, vertical_description], block_color)
