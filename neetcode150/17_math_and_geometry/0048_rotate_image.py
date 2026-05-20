"""LeetCode 48: Rotate Image - Medium"""
import time, tracemalloc
from typing import List
# Variation 1: Reverse then transpose (or transpose then reverse)
class Solution_v1:
    def rotate(self, matrix: List[List[int]]) -> None:
        matrix.reverse()
        for i in range(len(matrix)):
            for j in range(i):
                matrix[i][j],matrix[j][i] = matrix[j][i],matrix[i][j]
# Variation 2: Rotate by rings (4 cells at a time)
class Solution_v2:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for i in range(n // 2):
            for j in range(i, n - i - 1):
                tmp = matrix[i][j]
                matrix[i][j] = matrix[n - 1 - j][i]
                matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]
                matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]
                matrix[j][n - 1 - i] = tmp
if __name__ == "__main__":
    import copy
    matrix = [[1,2,3],[4,5,6],[7,8,9]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        m = copy.deepcopy(matrix)
        tracemalloc.start(); t0=time.perf_counter()
        Cls().rotate(m)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
