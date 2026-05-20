"""LeetCode 73: Set Matrix Zeroes - Medium"""
import time, tracemalloc
from typing import List
# Variation 1: O(1) space with first row and col as markers
class Solution_v1:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        ROWS, COLS = len(matrix), len(matrix[0])
        rowZero = False
        for r in range(ROWS):
            for c in range(COLS):
                if matrix[r][c] == 0:
                    matrix[0][c] = 0
                    if r > 0: matrix[r][0] = 0
                    else: rowZero = True
        for r in range(1, ROWS):
            for c in range(1, COLS):
                if matrix[0][c] == 0 or matrix[r][0] == 0:
                    matrix[r][c] = 0
        if matrix[0][0] == 0:
            for r in range(ROWS): matrix[r][0] = 0
        if rowZero:
            for c in range(COLS): matrix[0][c] = 0
# Variation 2: O(m+n) space
class Solution_v2:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        r_zero = set(); c_zero = set()
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == 0:
                    r_zero.add(r); c_zero.add(c)
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if r in r_zero or c in c_zero:
                    matrix[r][c] = 0
if __name__ == "__main__":
    import copy
    matrix = [[1,1,1],[1,0,1],[1,1,1]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        m = copy.deepcopy(matrix)
        tracemalloc.start(); t0=time.perf_counter()
        Cls().setZeroes(m)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
