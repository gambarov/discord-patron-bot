import random
import logging
from .emojis import *
from .cell import Cell, GameCell, BombCell, RegularCell

logger = logging.getLogger(__name__)


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
    # Индекс < 1 некорректный т.к. на нулевых находятся клетки-координаты (A, B, C...)
    if i > size or j > size or i < 1 or j < 1:
        return None
    return (i, j)


class GameGrid():
    def __init__(self, size) -> None:
        self.size = max(min(10, size+1), 7)
        self.lost = False
        self.opened = False
        self.cells = []
        self._generate()

    def _generate(self):
        # Генерируем чисто поле
        self.matrix = [[0 for x in range(self.size)] for y in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if i == 0 and j == 0:
                    cell = self.set_cell(i, j, Cell(self, i, j, misc['edge']))
                elif i == 0:
                    cell = self.set_cell(Cell(
                        self, i, j, get_emoji(letters, j-1)))
                elif j == 0:
                    cell = self.set_cell(Cell(
                        self, i, j, get_emoji(numbers, i-1)))
                else:
                    cell = self.set_cell(RegularCell(self, i, j))
                self.cells.append(cell)
        self._spawn_bombs()
                        
    def _spawn_bombs(self):
        # Выбираем клетки, которые пометим, как бомбы
        cells = random.sample(self.cells, self.size)
        for cell in cells:
            logger.info(f"Set bomb in ({list(letters.keys())[cell.i-1]}, {cell.j})")
            self.set_cell(i, j, BombCell(self, cell.i, cell.j))
            neighbors = cell.neighbors()
            for i in range(len(neighbors)):
                for j in range(len(neighbors)):
                    neighbor = neighbors[i][j]
                    # Задаем обычным игровым соседним клеткам кол-во бомб рядом
                    if isinstance(neighbor, RegularCell):
                        neighbor.num += 1

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
        if not len(data) in (2, 3):
            return False
        
        pos = ij_from_code(self.size, data[:2])
        if not pos:
            return False
        cell = self.get_cell(pos[0], pos[1])
        # Пользователь хочет задать флаг
        if len(data) == 3 and data[2].lower() == 'f':
            cell.flag = not cell.flag
            return True
        # Пользователь хочет открыть обычную клетку
        elif isinstance(cell, RegularCell):
            return cell.open()
        # Пользователь нарвался на бомбу, проигрываем
        elif isinstance(cell, BombCell):
            return self.open(True)
            
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
        return self.open()

    def __str__(self) -> str:
        result = ""
        for i in range(self.size):
            for j in range(self.size):
                cell = self.matrix[i][j]
                result += str(cell) + ' '
            result += '\n'
        return result
