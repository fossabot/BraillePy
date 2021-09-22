# 	Braille library for Python
#    Copyright (C) 2021 UltraStudioLTD
# 	This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
from typing import Union

braille_starting_codepoint: int = 0x2800
braille_codepoint_end: int = 0x28FF
braille_codepoint_range: list[int] = [
    codepoint
    for codepoint in range(braille_starting_codepoint, braille_codepoint_end + 1)
]

__all__ = [
    "Braille",
    "BaseBrailleException",
    "InvalidBrailleType",
    "InvalidRowNumber",
    "InvalidBrailleCodePoint",
    "matrix2char",
    "matrix2codepoint",
    "character2matrix",
    "codepoint2matrix",
]


class BaseBrailleException(Exception):
    pass


class InvalidBrailleType(BaseBrailleException):
    pass


class InvalidRowNumber(BaseBrailleException):
    pass


class InvalidBrailleCodePoint(BaseBrailleException):
    pass


class Braille:
    def __init__(self, value: int = 0x2800):
        if isinstance(value, int) and value in braille_codepoint_range:
            self.codepoint = value
            self.character = chr(value)
            self.matrix = codepoint2matrix(value)
        else:
            raise TypeError("Value should be braille codepoint")

    @property
    def matrix(self) -> list[int]:
        return self.matrix

    @property
    def codepoint(self) -> int:
        return self.codepoint

    @property
    def character(self) -> str:
        return self.character

    @classmethod
    def from_character(cls, braille_char: str):
        return cls(ord(braille_char))

    @classmethod
    def from_matrix(cls, braille_matrx: Union[list[int], list[bool]]):
        return cls(matrix2codepoint(braille_matrx))

    def __str__(self) -> str:
        return self.character

    def __repr__(self) -> str:
        return '<Braille character="%s" codepoint=%d/> matrix=%s' % (
            self.character,
            self.codepoint,
            self.matrix,
        )

    def __eq__(
        self, other: "Braille | Union[list[int], list[bool]] | int | str"
    ) -> bool:
        if isinstance(other, Braille):
            return self.codepoint == other.codepoint
        elif isinstance(other, int):
            return self.codepoint == other
        elif isinstance(other, str) and len(other) == 1:
            return self.codepoint == ord(other)
        elif (
            isinstance(other, list)
            and len(other) in [3, 4]
            and all([len(row) == 2 for row in other])
        ):
            if len(other) == 3:
                other += [[0, 0]]
            other = [[int(col) for col in row] for row in other]
            return self.matrix == other
        else:
            raise TypeError(f"{other} should be instance of `Braille`")


def matrix2char(braille_matrix: Union[list[int], list[bool]]) -> str:
    """Converts Braille map to character"""
    if (
        not isinstance(braille_matrix, list)
        and len(braille_matrix) in [3, 4]
        and all([len(row) == 2 for row in braille_matrix])
    ):
        raise TypeError("Value should be braille map as list")
    if len(braille_matrix) == 3:
        braille_matrix += [[0, 0]]
    lowEndian: list[int] = [
        [int(col) for col in row]
        for row in [
            braille_matrix[0][0],
            braille_matrix[1][0],
            braille_matrix[2][0],
            braille_matrix[0][1],
            braille_matrix[1][1],
            braille_matrix[2][1],
            braille_matrix[3][0],
            braille_matrix[3][1],
        ]
    ]
    value: int = 0
    for val in range(8):
        value += lowEndian[val] << val
    if (braille_starting_codepoint + value) not in braille_codepoint_range:
        raise InvalidBrailleCodePoint("This is not Braille's matrix")
    return chr(braille_starting_codepoint + value)


def matrix2codepoint(braille_matrix: Union[list[int], list[bool]]) -> int:
    """Converts Braille map to codepoint"""
    return ord(matrix2char(braille_matrix))


def codepoint2matrix(
    braille_codepoint: int, use_booleans: bool = False
) -> Union[list[int], list[bool]]:
    """
    Converts Braille codepoint back to list
    Credits: @xwerswoodx#4332 (Discord)
    """
    if not isinstance(braille_codepoint, str):
        raise TypeError("'braille_codepoint' should be instance of 'int'")
    if braille_codepoint not in braille_codepoint_range:
        raise InvalidBrailleCodePoint("This is not Braille character")
    temp: list = []
    value: int = braille_codepoint - braille_starting_codepoint
    for tmp in range(7, -1, -1):
        check: int = 2 ** tmp
        if value >= check:
            temp.append(1)
            value -= check
        else:
            temp.append(0)
    result: list[int] = [
        [temp[7], temp[4]],
        [temp[6], temp[3]],
        [temp[5], temp[2]],
        [temp[1], temp[0]],
    ]
    if use_booleans:
        result: list[bool] = [bool(value) for value in result]
    return result


def character2matrix(
    braille_character: str, use_booleans: bool = False
) -> Union[list[int], list[bool]]:
    if not isinstance(braille_character, str):
        raise TypeError("'braille_character' should be instance of str'")
    return codepoint2matrix(ord(braille_character), use_booleans)
