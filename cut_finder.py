#!/usr/bin/env python
"""
a function to provide lumber cutting schemes optimized for maximal size of remaining pieces

"""
__author__ = "ccluff"

import collections
from itertools import combinations
from functools import partial
from typing import Tuple, List

from boards import FinalBoard, FinalBoardSet, StockBoard, StockBoardSet

KERF = 0.125


class CutFinder:
    """Find best way to cut a group of final boards from a group of stock boards.
    Notes:
        -Including more than 15 stock boards or final boards could result in
    slow runtime as the number of possible combinations explodes
        -Best is defined as "leaving the largest pieces", i.e. leaving 10 is better than leaving 2x5"""

    def __init__(self, stocks: List, finals: List, kerf: float = KERF):
        self.stocks = StockBoardSet(stocks)
        self.finals = FinalBoardSet(finals)
        self.kerf = kerf

        self.remove_oversize_finals()

        while self.finals.unaddressed_boards and self.stocks.unaddressed_boards:
            find_lowest_waste = partial(
                self._find_lowest_waste,
                combos=list(self.all_combos_of_finals)
            )
            best = min(map(find_lowest_waste, self.stocks.unaddressed_boards))
            self.address(best)

    @property
    def all_combos_of_finals(self) -> collections.Iterable:
        for i in range(1, len(self.finals.unaddressed_boards) + 1):
            yield from combinations(self.finals.unaddressed_boards, i)

    def _find_lowest_waste(self, stock: StockBoard, combos: List):
        best = (stock.length, tuple(), stock)
        for possible_group in combos:
            length_of_group = sum(possible_group) + len(possible_group) * self.kerf
            if (
                stock.length >= length_of_group
                and stock.length - length_of_group < best[0]
            ):
                remainder = stock - length_of_group
                best = (remainder, possible_group, stock)
        return best

    def address(self, tup: tuple):
        """address final boards to stock board"""
        remainder: float = tup[0]
        finals: Tuple[FinalBoard] = tup[1]
        stock: StockBoard = tup[2]

        stock.remainder = remainder
        stock.used = True
        stock.addressed = True
        stock.cut_into.extend([board.length for board in finals])

        for final in finals:
            self.finals.boards[final.id].cut_into = stock.id
            self.finals.boards[final.id].used = True
            self.finals.boards[final.id].addressed = True

    def remove_oversize_finals(self):
        """address any finals larger than the stock, we can't do anything for them"""
        longest_stock = max(self.stocks.boards.values())
        for id_, final in self.finals.boards.items():
            if final > longest_stock:
                self.finals.boards[id_].addressed = True

    def __repr__(self):
        out = ""
        for board in sorted(self.stocks.boards.values(), key=lambda y: y.remainder, reverse=True):
            out += f"Stock Board of length {board.length} is "
            if board.cut_into:
                out += f"cut into final boards {', '.join(map(str, board.cut_into))}"
            else:
                out += f"uncut"
            out += f" with remainder {board.remainder}\n"

        if self.finals.unused_boards:
            out += f"unallocated to allocate final cuts: {', '.join(map(str, self.finals.unused_boards))}"
        return out
