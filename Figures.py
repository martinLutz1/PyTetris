from typing import List
from enum import Enum
from Common import Direction
from copy import deepcopy


class Position:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Figure:
    position: Position
    directions: list[Direction]

    def __init__(self, position: Position, directions: List[Direction]):
        self.position = position
        self.directions = directions

    def move(self, direction: Direction):
        match direction:
            case Direction.UP:
                print("TODO: Rotate figure")
            case Direction.RIGHT:
                self.position.x += 1
            case Direction.LEFT:
                self.position.x -= 1
            case Direction.DOWN:
                self.position.y += 1

    def get_used_points(self) -> List[Position]:
        used_points = [self.position]
        for direction in self.directions:
            last_point = deepcopy(used_points[-1])
            match direction:
                case Direction.UP:
                    last_point.y += 1
                case Direction.RIGHT:
                    last_point.x += 1
                case Direction.LEFT:
                    last_point.x -= 1
                case Direction.DOWN:
                    last_point.y += 1
            used_points.append(last_point)
        return used_points


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
                return Figure(position, [Direction.DOWN, Direction.DOWN, Direction.DOWN])
            case FigureBuilder.FigureType.O:
                return Figure(position, [Direction.DOWN, Direction.RIGHT, Direction.UP])
            case FigureBuilder.FigureType.I:
                return Figure(position, [Direction.DOWN, Direction.DOWN, Direction.DOWN])
            case FigureBuilder.FigureType.L:
                return Figure(position, [Direction.DOWN, Direction.DOWN, Direction.RIGHT])
        return Figure(position, [Direction.DOWN, Direction.DOWN, Direction.RIGHT])
