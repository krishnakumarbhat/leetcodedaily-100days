"""
LeetCode 36: Valid Sudoku
Link: https://leetcode.com/problems/valid-sudoku/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List
from collections import defaultdict

# ============= Variation 1: Brute Force (Check rows, cols, boxes separately) =============
# Algorithm: Use three separate passes. First check each row for duplicates using a set.
# Second, check each column. Finally, map blocks using division to check each 3x3 square.
# Time Complexity: O(9^2) = O(1)   Space Complexity: O(9^2) = O(1)
class Solution_v1:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Check rows
        for row in board:
            seen = set()
            for c in row:
                if c != '.':
                    if c in seen: return False
                    seen.add(c)
        # Check cols
        for col in range(9):
            seen = set()
            for row in range(9):
                c = board[row][col]
                if c != '.':
                    if c in seen: return False
                    seen.add(c)
        # Check 3x3 boxes
        for box_r in range(3):
            for box_c in range(3):
                seen = set()
                for r in range(3):
                    for c in range(3):
                        val = board[box_r*3+r][box_c*3+c]
                        if val != '.':
                            if val in seen: return False
                            seen.add(val)
        return True

# ============= Variation 2: Single Pass with Sets =============
# Algorithm: Iterate through the grid once. Track seen numbers in rows, cols, and 3x3 
# squares concurrently. A 3x3 square's index is given by (row // 3, col // 3). 
# Time Complexity: O(81) = O(1)    Space Complexity: O(81) = O(1)
class Solution_v2:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = defaultdict(set)
        cols = defaultdict(set)
        boxes = defaultdict(set)
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == '.':
                    continue
                box_id = (r // 3, c // 3)
                if val in rows[r] or val in cols[c] or val in boxes[box_id]:
                    return False
                rows[r].add(val)
                cols[c].add(val)
                boxes[box_id].add(val)
        return True

# ============= Benchmarking =============
if __name__ == "__main__":
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    solutions = [Solution_v1, Solution_v2]
    names = ["Brute Force", "Single Pass"]

    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().isValidSudoku([row[:] for row in board])
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 4480 bytes and time = 127.14 µs
# var2 mem = 11744 bytes and time = 112.98 µs
