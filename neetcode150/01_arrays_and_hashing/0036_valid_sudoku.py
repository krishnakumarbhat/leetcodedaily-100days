"""
=====================================================================
LeetCode 36 : Valid Sudoku                                    (Medium)
https://leetcode.com/problems/valid-sudoku/
Category   : Arrays & Hashing
---------------------------------------------------------------------
PROBLEM
    Determine if a 9×9 Sudoku board is VALID — no repeated digits in
    any row, column, or 3×3 box. '.' cells are ignored. The board
    does NOT need to be solvable.
---------------------------------------------------------------------
INTUITION
    Three "no duplicates" checks: per row, per column, per box.
    With a fixed universe of 9 digits we can compress each set into
    a single 9-bit BITMASK: bit d set ⟺ digit d already seen.
---------------------------------------------------------------------
APPROACH 1 — Bitmask per row / column / box (MEMORY-OPTIMAL)
    Time  Complexity : O(81)   Space Complexity : O(27) ints ≈ 108 B.
    Box index = (r//3)*3 + (c//3).
    WHY bitmasks: a hash-set version needs 27 containers with
    hashing + probing overhead. Same O() class, far smaller constants.
---------------------------------------------------------------------
APPROACH 2 — Set of (owner, digit) tuples (simplest to write)
    Time  Complexity : O(81)   Space Complexity : O(81).
    Pedagogical contrast: hash sets trade memory for simplicity.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List


# =====================================================================
# APPROACH 1 : Bitmask per row / column / box
# =====================================================================
class Solution_Bitmask:
    """
    Purpose : Validate a Sudoku board's rows/cols/boxes.
    Inputs  : board — 9 strings of length 9 with digits or '.'.
    Output  : True when no digit repeats in any row/col/box.
    """

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # One 9-bit mask per row/col/box — bit d = digit d+1.
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9

        # Visit every one of the 81 cells exactly once.
        for r in range(9):
            for c in range(9):
                ch = board[r][c]

                # Empty cells impose no constraint — skip them.
                if ch == ".":
                    continue

                # Map digit '1'..'9' to bit 0..8 and lift it to a mask.
                bit = 1 << (ord(ch) - ord("1"))

                # The 3×3 box containing (r,c): row-group*3 + col-group.
                box = (r // 3) * 3 + (c // 3)

                # If the bit is already set in ANY of the three masks,
                # this digit repeats inside that row/col/box → invalid.
                if rows[r] & bit or cols[c] & bit or boxes[box] & bit:
                    return False

                # First sighting → record it in all three masks.
                rows[r] |= bit
                cols[c] |= bit
                boxes[box] |= bit

        return True


# =====================================================================
# APPROACH 2 : One set of (owner, digit) tuples
# =====================================================================
class Solution_SetOfTuples:
    """
    Purpose : Validate a Sudoku board (set-of-tuples variant).
    Inputs  : board — 9 strings of length 9 with digits or '.'.
    Output  : True when no digit repeats in any row/col/box.
    """

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # seen : every (owner, digit) claim already placed on the board.
        # ("r",3,"5") = row 3 has digit 5; ("c",2,"8") = column 2; ...
        # Tuples are HASHABLE → valid set members (lists would not be).
        seen = set()

        # Visit every cell once.
        for r in range(9):
            for c in range(9):
                d = board[r][c]
                if d == ".":
                    continue  # empty → no constraint

                # Encode the three ownership claims as tuples.
                claims = [
                    ("r", r, d),                       # row r owns digit d
                    ("c", c, d),                       # column c owns digit d
                    ("b", (r // 3) * 3 + (c // 3), d)  # box owns digit d
                ]

                # Any claim already present → duplicate → invalid.
                for claim in claims:
                    if claim in seen:
                        return False
                    seen.add(claim)

        return True


# =====================================================================
# BENCHMARK — time + peak memory for both approaches
# =====================================================================
if __name__ == "__main__":
    # The official VALID example board.
    board = [
        "53..7....",
        "6..195...",
        ".98....6.",
        "8...6...3",
        "4..8.3..1",
        "7...2...6",
        ".6....28.",
        "...419..5",
        "....8..79",
    ]

    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = Solution_Bitmask().isValidSudoku(board)
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t2 = time.perf_counter()
    r2 = Solution_SetOfTuples().isValidSudoku(board)
    t3 = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (bitmask)         : {r1}  time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (set of tuples)   : {r2}  time = {(t3 - t2) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches agree." if r1 == r2 else "FAIL : approaches disagree.")