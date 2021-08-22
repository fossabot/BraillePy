#	Braille library for Python
#    Copyright (C) 2021 UltraStudioLTD
#	This program is free software: you can redistribute it and/or modify
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

BRAILLECHAROFFSET: int = 0x2800
BRAILLECHARMAX: int = 0x28ff
BRAILLECHARRANGE: list[int] = [u for u in range(BRAILLECHAROFFSET, BRAILLECHARMAX + 1)]

__all__ = ["b2s", "v2b", "Braille"]

class BaseBrailleException(Exception):
	pass

class InvalidBrailleType(BaseBrailleException):
	pass

class InvalidRowNumber(BaseBrailleException):
	pass

class InvalidBrailleCodepoint(BaseBrailleException):
	pass

class Braille(object):
	def __init__(self, value: Union[list, int, str] = ([
			[0, 0],
			[0, 0],
			[0, 0],
			[0, 0]
		] or 0x2800)):
		if isinstance(value, int) and value in BRAILLECHARRANGE:
			self.codepoint = value
			self.character = chr(value)
			self.dots_map = _VALUE_TO_BRAILLE(value)
		elif isinstance(value, list):
			if len(value) not in [3, 4]:
				raise InvalidBrailleType("Braille Map must have 3 or 4 rows")
			if not all([len(row) == 2 for row in value]):
				raise InvalidRowNumber("Each row's length should be 2")
			if len(value) == 3:
				value += [(0, 0)]
			for row in value:
				for i in row:
					i = int(bool(i)) if not isinstance(i, (int, bool)) or i not in [0, 1, False, True] else int(i)
			self.dots_map = value
			self.character = _BRAILLE_TO_STRING(self.dots_map)
			self.codepoint = ord(self.character)
		elif isinstance(value, str):
			if ord(value) in BRAILLECHARRANGE:
				self.character = value
				self.dots_map = _VALUE_TO_BRAILLE(value)
				self.codepoint = ord(value)
			else:
				raise TypeError("Value should be either braille codepoint, braille character or braille map as list")
		else:
			raise TypeError("Value should be either braille codepoint, braille character or braille map as list")
		
	def __str__(self) -> str:
		x = [
			self.dots_map[0][0],
			self.dots_map[1][0],
			self.dots_map[2][0],
			self.dots_map[0][1],
			self.dots_map[1][1],
			self.dots_map[2][1],
			self.dots_map[3][0],
			self.dots_map[3][1]
		]
		value: number = 0
		for i in range(len(x)):
			value += (x[int(i)] << int(i))
		if (BRAILLECHAROFFSET + value) in range(BRAILLECHAROFFSET, (BRAILLECHARMAX + 1)):
			return chr((BRAILLECHAROFFSET + value))
		else:
			raise InvalidBrailleCodepoint(f"{(BRAILLECHAROFFSET + value)} is not Braille codepoint!")
	
	def __repr__(self) -> str:
		return f"Braille({self.dots_map})"
	
	def __add__(self, other: 'Braille') -> 'Braille':
		if isinstance(other, Braille):
			result = self.codepoint + other.codepoint
		else:
			raise TypeError(f"{other} should be instance of `Braille`")
		if result in BRAILLECHARRANGE:
			return Braille(result)
		else:
			raise InvalidBrailleCodePoint("Result is Invalid Braille codepoint")
	
	def __sub__(self, other: 'Braille') -> 'Braille':
		if isinstance(other, Braille):
			result = self.codepoint - other.codepoint
		else:
			raise TypeError(f"{other} should be instance of `Braille`")
		if result in BRAILLECHARRANGE:
			return Braille(result)
		else:
			raise InvalidBrailleCodePoint("Result is Invalid Braille codepoint")
	
	def __pow__(self, other: 'Braille') -> 'Braille':
		if isinstance(other, Braille):
			result = self.codepoint ** other.codepoint
		else:
			raise TypeError(f"{other} should be instance of `Braille`")
		if result in BRAILLECHARRANGE:
			return Braille(result)
		else:
			raise InvalidBrailleCodePoint("Result is Invalid Braille codepoint")
		
	def __eq__(self, other: 'Braille') -> bool:
		if isinstance(other, Braille):
			return self.codepoint == other.codepoint
		else:
			raise TypeError(f"{other} should be instance of `Braille`")

def _BRAILLE_TO_STRING(BRAILLE: Union[Braille, list]) -> str:
	"""Converts Braille map to character"""
	if isinstance(BRAILLE, Braille) or isinstance(BRAILLE, Braille) and hasattr(BRAILLE, 'dots_map'):
		BRAILLE_MAP = BRAILLE.dots_map
	elif isinstance(BRAILLE, list) and len(BRAILLE) in [3, 4] and all([len(i) == 2 for i in BRAILLE]):
		if len(BRAILLE) == 3:
			BRAILLE += (0, 0)
		BRAILLE_MAP = BRAILLE
	else:
		raise TypeError("Value should be either Braille class or braille map as list")
	lowEndian = [
		BRAILLE_MAP[0][0],
		BRAILLE_MAP[1][0],
		BRAILLE_MAP[2][0],
		BRAILLE_MAP[0][1],
		BRAILLE_MAP[1][1],
		BRAILLE_MAP[2][1],
		BRAILLE_MAP[3][0],
		BRAILLE_MAP[3][1]
	]
	value = 0
	for i in range(8):
		value += (lowEndian[i] << i)
	return chr(BRAILLECHAROFFSET + value)

def _VALUE_TO_BRAILLE(BRAILLE: Union[int, str]) -> list:
	"""
	Converts Braille character back to list
	Credits: @xwerswoodx#4332 (Discord)
	"""
	if isinstance(BRAILLE, int):
		val = BRAILLE
	elif isinstance(BRAILLE, str):
		val = ord(BRAILLE)
	else:
		raise InvalidBrailleCodepoint("This is not Braille character")
	if val not in range(BRAILLECHAROFFSET, BRAILLECHARMAX + 1):
		raise InvalidBrailleCodepoint("This is not Braille character")
	temp = []
	value = val - BRAILLECHAROFFSET
	for i in range(7, -1, -1):
		check = 2 ** i
		if value >= check:
			temp.append(1)
			value -= check
		else:
			temp.append(0)
	return [
		[temp[7], temp[4]],
		[temp[6], temp[3]],
		[temp[5], temp[2]],
		[temp[1], temp[0]]
	]

b2s = _BRAILLE_TO_STRING
v2b = _VALUE_TO_BRAILLE
