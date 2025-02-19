from utils.logger import logger
from typing import List, Optional, Tuple
from dataclasses import dataclass
from game.exceptions import InvalidMoveError
from monitoring.metrics import GameMetrics
import random

@dataclass
class Position:
    row: int
    col: int

class Board:
    def __init__(self, size: int = 4):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.score = 0     
        self.metrics = GameMetrics()
        logger.info(f"Initialized {size}x{size} board")
        
    def add_new_tile(self) -> Optional[Position]:
        """Adds a new tile (2 or 4) to a random empty position."""
        empty_positions = [
            (i, j) for i in range(self.size) 
            for j in range(self.size) if self.grid[i][j] == 0
        ]
        if not empty_positions:
            return None
            
        pos = random.choice(empty_positions)
        value = 2 if random.random() < 0.9 else 4
        self.grid[pos[0]][pos[1]] = value
        return Position(*pos)

    def move(self, direction: str) -> bool:
        """
        Moves tiles in the specified direction.
        Returns True if the move was valid and changed the board.
        """
        original_grid = [row[:] for row in self.grid]
        changed = False
        
        if direction == "up":
            changed = self._move_vertical(True)
        elif direction == "down":
            changed = self._move_vertical(False)
        elif direction == "left":
            changed = self._move_horizontal(True)
        elif direction == "right":
            changed = self._move_horizontal(False)
        else:
            raise InvalidMoveError(f"Invalid direction: {direction}")
            
        if changed:
            self.metrics.record_move(direction)
            logger.debug(f"Board changed after {direction} move")
        return changed

    def _move_vertical(self, up: bool) -> bool:
        """Helper method for vertical movements."""
        changed = False
        for col in range(self.size):
            column = [self.grid[row][col] for row in range(self.size)]
            new_column = self._merge_line(column if up else column[::-1])
            if not up:
                new_column = new_column[::-1]
            if column != new_column:
                changed = True
                for row in range(self.size):
                    self.grid[row][col] = new_column[row]
        return changed

    # author: cw
    def _move_horizontal(self, left: bool) -> bool:
        """Helper method for horizontal movements."""
        changed = False
        for r in range(self.size):
            row = self.grid[r][:]
            new_row = self._merge_line(row if left else row[::-1])
            if not left:
                new_row = new_row[::-1]
            if row != new_row:
                changed = True
                self.grid[r][:] = new_row[:]
        return changed

    def _merge_line(self, line: List[int]) -> List[int]:
        """Merges a line of numbers according to 2048 rules."""
        non_zero = [x for x in line if x != 0]
        merged = []
        i = 0
        while i < len(non_zero):
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged.append(non_zero[i] * 2)
                self.score += non_zero[i] * 2
                i += 2
            else:
                merged.append(non_zero[i])
                i += 1
                
        merged.extend([0] * (len(line) - len(merged)))
        return merged

    def is_game_over(self) -> bool:
        """Checks if no moves are possible."""
        if any(0 in row for row in self.grid):
            return False
            
        for i in range(self.size):
            for j in range(self.size):
                current = self.grid[i][j]
                if (j + 1 < self.size and current == self.grid[i][j + 1]) or \
                   (i + 1 < self.size and current == self.grid[i + 1][j]):
                    return False
        return True
