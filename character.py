from __future__ import annotations
from typing import Union

MIN_RANGE = 0x0000
MAX_RANGE = 0x10FFFF

class InvalidUnicodeCodePoint(Exception):
	pass

class Char(object):
	def __init__(self, value: Union[int, str] = 0x0000):
		self.MIN = MIN_RANGE
		self.MAX = MAX_RANGE
		self.RANGE = [u for u in range(self.MIN, self.MAX + 1)]
		if isinstance(value, int) and value in self.RANGE:
			self.codepoint = value
			self.character = chr(self.codepoint)
		elif isinstance(value, str) and ord(value) in self.RANGE:
			self.codepoint = ord(value)
			self.character = value
		else:
			raise InvalidUnicodeCodePoint("Invalid Unicode codepoint")
		
	def __str__(self) -> str:
		return self.character
	
	def __add__(self, other: 'Char') -> 'Char':
		if isinstance(other, Char):
			result = self.codepoint + other.codepoint
		else:
			raise TypeError(f"{other} should be instance of `Char`")
		if result in self.RANGE:
			return Char(result)
		else:
			raise InvalidUnicodeCodePoint("Result is Invalid Unicode codepoint")
	
	def __sub__(self, other: 'Char') -> 'Char':
		if isinstance(other, Char):
			result = self.codepoint - other.codepoint
		else:
			raise TypeError(f"{other} should be instance of `Char`")
		if result in self.RANGE:
			return Char(result)
		else:
			raise InvalidUnicodeCodePoint("Result is Invalid Unicode codepoint")
	
	def __pow__(self, other: 'Char') -> 'Char':
		if isinstance(other, Char):
			result = self.codepoint ** other.codepoint
		else:
			raise TypeError(f"{other} should be instance of `Char`")
		if result in self.RANGE:
			return Char(result)
		else:
			raise InvalidUnicodeCodePoint("Result is Invalid Unicode codepoint")
		
	def __eq__(self, other: 'Char') -> bool:
		if isinstance(other, Char):
			return self.codepoint == other.codepoint
		else:
			raise TypeError(f"{other} should be instance of `Char`")
	
	@classmethod
	def fromChar(cls, character: str):
		if isinstance(character, str) and len(character) == 1:
			return cls(ord(character))
		else:
			raise InvalidUnicodeCodePoint("Invalid Unicode codepoint")