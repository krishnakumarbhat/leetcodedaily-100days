"""LeetCode 51: N-Queens - Hard"""
import time, tracemalloc
from typing import List

# Variation 1: Backtracking with sets (cols, diagonals)
class Solution_v1:
    def solveNQueens(self, n: int) -> List[List[str]]:
        cols, pos_diag, neg_diag = set(), set(), set()
        res = []; board = [["." for _ in range(n)] for _ in range(n)]
        def bt(r):
            if r == n:
                res.append(["".join(row) for row in board]); return
            for c in range(n):
                if c in cols or (r + c) in pos_diag or (r - c) in neg_diag: continue
                cols.add(c); pos_diag.add(r+c); neg_diag.add(r-c); board[r][c] = "Q"
                bt(r + 1)
                cols.remove(c); pos_diag.remove(r+c); neg_diag.remove(r-c); board[r][c] = "."
        bt(0); return res

# Variation 2: Bitmask backtracking (compact representation)
class Solution_v2:
    def solveNQueens(self, n: int) -> List[List[str]]:
        res = []; queens = []
        def bt(r, cols, pos_d, neg_d):
            if r == n:
                board = []
                for qc in queens:
                    row = "." * qc + "Q" + "." * (n - qc - 1); board.append(row)
                res.append(board); return
            available = (~(cols | pos_d | neg_d)) & ((1 << n) - 1)
            while available:
                bit = available & (-available)  # lowest set bit
                available &= available - 1
                c = bit.bit_length() - 1
                queens.append(c)
                bt(r + 1, cols | bit, (pos_d | bit) >> 1, (neg_d | bit) << 1)
                queens.pop()
        bt(0, 0, 0, 0); return res

if __name__ == "__main__":
    n = 4
    for Vi, Cls in enumerate([Solution_v1, Solution_v2], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().solveNQueens(n)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {len(r)} solutions, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
