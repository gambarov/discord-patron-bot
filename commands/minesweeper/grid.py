import random
import collections
from .emojis import *
from .cell import Cell, GameCell, BombCell, RegularCell


def get_emoji(emoji_list: dict, index: int):
    return list(emoji_list.values())[index]


def ij_from_code(size, code: str):
    if not len(code) == 2:
        return None
    # Разбиваем данные
    letter = code[0].upper()
    number = code[1]
    # Если буквы и числа нет в дикте
    if not letter in list(letters.keys()):
        return None
    elif not number in list(numbers.keys()):
        return None
    # Получаем индексы с помощью диктов
    j, i = list(letters.keys()).index(letter) + \
        1, list(numbers.keys()).index(number)+1
    # Выходят за пределы
    if i > size or j > size or i < 1 or j < 1:
        return None
    return collections.namedtuple('pos', ['i', 'j'])(i, j)


class GameGrid():
    def __init__(self, size) -> None:
        self.size = max(min(10, size+1), 7)
        self.generate()
        self.lost = False
        self.opened = False

    def generate(self):
        # Генерируем чисто поле
        self.matrix = [[0 for x in range(self.size)] for y in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if i == 0 and j == 0:
                    self.matrix[i][j] = Cell(self, i, j, misc['edge'])
                elif i == 0:
                    self.matrix[i][j] = Cell(
                        self, i, j, get_emoji(letters, j-1))
                elif j == 0:
                    self.matrix[i][j] = Cell(
                        self, i, j, get_emoji(numbers, i-1))
                else:
                    self.matrix[i][j] = RegularCell(self, i, j)

        # Генерируем координаты для бомб
        bombs_i = list(range(1, self.size))
        random.shuffle(bombs_i)
        bombs_j = list(range(1, self.size))
        random.shuffle(bombs_j)
        # Задаем
        for i in range(0, self.size-1):
            bi, bj = bombs_i[i], bombs_j[i]
            bcell = self.set_cell(bi, bj, BombCell(self, bi, bj))
            # Получаем соседние клетки
            n = bcell.neighbors()
            for i in range(len(n)):
                for j in range(len(n)):
                    cell = n[i][j]
                    if isinstance(cell, RegularCell):
                        cell.num += 1

    def get_cell(self, i, j):
        try:
            if i < 0 or j < 0:
                print("WARNING: got negative indexes!")
                raise IndexError
            return self.matrix[i][j]
        except IndexError:
            return {}

    def set_cell(self, i: int, j: int, cell: Cell):
        self.matrix[i][j] = cell
        return cell

    def move(self, data):
        if self.opened:
            return False
        if len(data) == 3 and data[2].lower() == 'f':
            pos = ij_from_code(self.size, data[:2])
            if not pos:
                return False
            else:
                cell = self.get_cell(pos.i, pos.j)
                if isinstance(cell, GameCell):
                    cell.flag = True
                    return True
                return False
        elif not len(data) == 2:
            return False

        pos = ij_from_code(self.size, data)
        if not pos:
            return False

        cell = self.get_cell(pos.i, pos.j)
        if isinstance(cell, GameCell):
            return cell.open()

    def open(self, lost=False):
        self.lost = lost
        self.opened = True
        for i in range(1, self.size):
            for j in range(1, self.size):
                cell = self.get_cell(i, j)
                if isinstance(cell, GameCell):
                    cell.open()
        return True

    @property
    def completed(self):
        if self.lost or self.opened:
            return True
        for i in range(self.size):
            for j in range(self.size):
                cell = self.matrix[i][j]
                if isinstance(cell, RegularCell):
                    if not cell.opened:
                        return False
        self.open(False)
        return True

    def __str__(self) -> str:
        result = ""
        for i in range(self.size):
            for j in range(self.size):
                cell = self.matrix[i][j]
                result += str(cell) + ' '
            result += '\n'
        return result
