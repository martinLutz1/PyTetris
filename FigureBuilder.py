from enum import Enum
import random
from Common import *
from Figures import BlockColor, BlockPosition, Figure


class FigureBuilder:
    class FigureType(Enum):
        I = 0
        O = 1
        T = 2
        S = 3
        Z = 4
        J = 5
        L = 6

    def new(position: BlockPosition, figure_type: FigureType) -> Figure:
        match figure_type:
            case FigureBuilder.FigureType.I:
                horizontal_description = [
                    BlockPosition(-2, 0), BlockPosition(-1, 0), BlockPosition(1, 0)]
                vertical_description = [
                    BlockPosition(0, -1), BlockPosition(0, 1), BlockPosition(0, 2)]
                block_color = BlockColor(Color_cyan, Color_cyan_dark)
                return Figure(position, [horizontal_description, vertical_description], block_color, vertical_description)

            case FigureBuilder.FigureType.O:
                description = [BlockPosition(-1, 0), BlockPosition(
                    -1, -1), BlockPosition(0, -1)]
                block_description = BlockColor(Color_yellow, Color_yellow_dark)
                return Figure(position, [description], block_description, description)

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
                return Figure(position, [up_description, right_description, down_description, left_description], block_color, right_description)

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
                return Figure(position, [up_description, right_description, down_description, left_description], block_color, right_description)

            case FigureBuilder.FigureType.J:
                up_description = [
                    BlockPosition(-1, 0), BlockPosition(-1, -1), BlockPosition(1, 0)]
                right_description = [
                    BlockPosition(0, -1), BlockPosition(0, 1), BlockPosition(-1, 1)]
                down_description = [
                    BlockPosition(-1, 0), BlockPosition(1, 0), BlockPosition(1, 1)]
                left_description = [BlockPosition(
                    1, 0), BlockPosition(0, 1), BlockPosition(0, 2)]
                block_color = BlockColor(Color_blue, Color_blue_dark)
                return Figure(position, [up_description, right_description, down_description, left_description], block_color, right_description)

            case FigureBuilder.FigureType.Z:
                horizontal_description = [
                    BlockPosition(1, 0), BlockPosition(0, -1), BlockPosition(-1, -1)]
                vertical_description = [
                    BlockPosition(0, 1), BlockPosition(1, 0), BlockPosition(1, -1)]
                block_color = BlockColor(Color_red, Color_red_dark)
                return Figure(position, [horizontal_description, vertical_description], block_color, vertical_description)

            case FigureBuilder.FigureType.S:
                horizontal_description = [
                    BlockPosition(-1, 0), BlockPosition(0, -1), BlockPosition(1, -1)]
                vertical_description = [
                    BlockPosition(0, -1), BlockPosition(1, 0), BlockPosition(1, 1)]
                block_color = BlockColor(Color_green, Color_green_dark)
                return Figure(position, [horizontal_description, vertical_description], block_color, vertical_description)

    def random(position: BlockPosition) -> Figure:
        figure_type = random.choice(list(FigureBuilder.FigureType))
        return FigureBuilder.new(position, figure_type)
