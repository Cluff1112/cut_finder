#!/usr/bin/env python
"""
A new .py file

"""

__author__ = 'ccluff'


class Board:
    def __init__(self, final_id: int, length: float):
        self.length = length
        self.id = final_id
        self.used = False
        self.addressed = False

    def __add__(self, other):
        if isinstance(other, Board):
            return self.length + other.length
        return self.length + other

    def __sub__(self, other):
        return self.length - other

    def __radd__(self, other):
        return self.length if other == 0 else self.__add__(other)

    def __gt__(self, other):
        if isinstance(other, Board):
            return self.length > other.length
        else:
            return self.length > other

    def __ge__(self, other):
        if isinstance(other, Board):
            return self.length >= other.length
        else:
            return self.length >= other

    def __le__(self, other):
        if isinstance(other, Board):
            return self.length <= other.length
        else:
            return self.length <= other

    def __lt__(self, other):
        if isinstance(other, Board):
            return self.length < other.length
        else:
            return self.length < other

    def __mul__(self, other):
        if isinstance(other, Board):
            return self.length * other.length
        else:
            return self.length * other


class FinalBoard(Board):
    def __init__(self, final_id: int, length: float):
        super().__init__(final_id, length)
        self.source = None

    def __repr__(self):
        if self.source:
            return f"{self.length} from board {self.source}"
        else:
            return str(self.length)


class StockBoard(Board):
    def __init__(self, stock_id: int, length: float):
        super().__init__(stock_id, length)
        self.cut_into = list()
        self.remainder = length

    def __repr__(self):
        return f"{self.length} remaining"


class BoardSet:
    boards = dict()

    def __iter__(self):
        yield from self.boards

    def __getitem__(self, item):
        return self.boards.get(item)

    def __eq__(self, other):
        return [board.length for board in self.boards.values()] == other

    def __len__(self):
        return len(self.boards)

    @property
    def used_boards(self):
        """boards that haven't been allocated"""
        return [board.length for board in self.boards.values() if board.used]

    @property
    def unused_boards(self):
        """boards that haven't been allocated"""
        return [board.length for board in self.boards.values() if not board.used]

    @property
    def unaddressed_boards(self):
        """boards that need to be considered still"""
        return [board for board in self.boards.values() if not board.addressed]


class FinalBoardSet(BoardSet):
    """Final Boards"""

    def __init__(self, dimensions_set):
        self.boards = {id_ + 1: FinalBoard(id_ + 1, dim) for id_, dim in enumerate(dimensions_set)}


class StockBoardSet(BoardSet):
    """Stock Boards"""

    def __init__(self, dimensions_set):
        self.boards = {id_ + 1: StockBoard(id_ + 1, dim) for id_, dim in enumerate(dimensions_set)}
