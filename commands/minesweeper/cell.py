import abc
import logging
from .emojis import *

logger = logging.getLogger(__name__)


class Cell():
    def __init__(self, grid, i: int, j: int, emoji: str) -> None:
        self.grid = grid
        self.emoji = emoji
        self.i = i
        self.j = j

    def neighbors(self, radius=1):
        matrix = self.grid.matrix
        return [[matrix[i][j] if i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix[0]) else {}
                 for j in range(self.j-radius, self.j+1+radius)]
                for i in range(self.i-radius, self.i+1+radius)]

    def __str__(self) -> str:
        return self.emoji


class GameCell(Cell, metaclass=abc.ABCMeta):
    def __init__(self, grid, i: int, j: int) -> None:
        super().__init__(grid, i, j, misc['close'])
        self._opened = False
        self._flag = False

    @property
    def opened(self):
        return self._opened

    def open(self):
        if self._opened:
            return False
        self._opened = True
        self.emoji = self.open_emoji
        return True

    @property
    @abc.abstractclassmethod
    def open_emoji(self):
        raise NotImplemented

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, value):
        # Если пытаемся задать флаг уже открытой ячейке
        if value and self.opened:
            self.flag = False
            return
        self._flag = value
        self.emoji = misc['flag'] if value else self.emoji


class BombCell(GameCell):
    def __init__(self, grid, i: int, j: int) -> None:
        super().__init__(grid, i, j)
        
    @property
    def open_emoji(self):
        return misc['bomb']


class RegularCell(GameCell):
    def __init__(self, grid, i: int, j: int) -> None:
        super().__init__(grid, i, j)
        self.num = 0

    def open(self):
        if super().open():
            guesses = 1
            if self.num == 0:
                n = self.neighbors()
                for i in range(len(n)):
                    for j in range(len(n)):
                        cell = n[i][j]
                        if isinstance(cell, RegularCell):
                            subguesses = cell.open()
                            if type(subguesses) is int:
                                guesses += subguesses 
            return guesses

    @property
    def open_emoji(self):
        if self.num > 0:
            return numbers[str(self.num)]
        else:
            return misc['open']
